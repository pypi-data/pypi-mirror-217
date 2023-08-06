import os
from queue import Queue, Empty
import threading
from typing import Callable, Optional, Dict
from time import perf_counter
import requests
import uuid
from enum import Enum
from dotenv import load_dotenv
import logging
from hegel.utils import set_environment, get_current_time_millis, get_present_date

# Load environmental variables from `.env` file
load_dotenv()
set_environment()


class TaskTypes(Enum):
    CREATE = 1
    UPDATE = 2


class HegelScribe:
    r"""
    ``Scribe`` helps record the input and response of a LLM call with
    minimal overhead. The call to the LLM's API is not routed through our server;
    only the input and response are captured and written to the database
    through a separate thread without blocking the main thread.

    Args:
        name (str): the name that you want to associate this model with.
        completion_fn (Callable): the function that will be invoked with a prompt and parameters,
            returning a response from the LLM (e.g. ``openai.ChatCompletion.create``)
        session_id (Optional[int]): if this instance is associated with a specific session or user
            you can pass that in there as well
        custom_metrics (Optional[Dict[str, Callable]]): dictionary of custom metric names and the functions
            to compute the metric. Each function should take in `(input, response)` pair from the LLM model,
            and return a value. The results will be computed and sent to the database.

    Example:
        >>> import openai
        >>> scribe = HegelScribe(name="Helpful Assistant", completion_fn=openai.ChatCompletion.create)
        >>> response = scribe(
        >>>     model= "gpt-3.5-turbo",
        >>>     messages = [
        >>>         {"role": "system", "content": "You are a helpful assistant."},
        >>>         {"role": "user", "content": "Who won the world series in 2020?"},
        >>> ])
    """

    def __init__(
        self,
        name: str,
        completion_fn: Callable,
        track_feedback: Optional[bool] = False,
        session_id: Optional[str] = None,
        custom_metrics: Optional[Dict[str, Callable]] = None,
    ):
        self.url = os.getenv("HEGELAI_URL")
        self.feedback_url = os.getenv("HEGELAI_FEEDBACK_URL")
        self.api_key = os.getenv("HEGELAI_API_KEY")
        self.model_name: str = name
        self.session_id: str = session_id
        self.track_feedback = track_feedback
        self.completion_fn = completion_fn

        self.data_queue = Queue()
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()
        self.custom_metrics: Dict[str, Callable] = (
            {} if custom_metrics is None else custom_metrics
        )

    @staticmethod
    def create_session_id():
        return str(uuid.uuid4())

    @staticmethod
    def _check_response(response):
        if not response.ok:
            logging.warning(
                "Error while logging: "
                + str(response.status_code)
                + ": "
                + str(response.reason)
            )

    def _enqueue(self, task_type, task_params) -> None:
        self.data_queue.put((task_type, task_params))

    def _compute_custom_metrics(self, input, response):
        res = {}
        for metric_name, fn in self.custom_metrics.items():
            res[metric_name] = fn(input, response)
        return res

    def _process_queue(self) -> None:
        while self.is_running:
            try:
                item = self.data_queue.get(timeout=0.2)
                if item[0] == TaskTypes.CREATE:
                    (_, params) = item
                    log_id, input, response, latency, timestamp, date = params
                    custom_metric_values = self._compute_custom_metrics(input, response)
                    self._record(
                        log_id,
                        input,
                        response,
                        latency,
                        timestamp,
                        date,
                        custom_metric_values,
                    )
                else:
                    (_, params) = item
                    log_id, feedback, timestamp, date = params
                    self._record_feedback(log_id, feedback, timestamp, date)
                self.data_queue.task_done()
            except Empty:
                continue

    def _record_feedback(self, log_id, feedback, timestamp, date) -> None:
        payload = {
            "log_id": log_id,
            "model_name": self.model_name,
            "metadata": feedback,
            "timestamp": timestamp,
            "date": date,
        }
        headers = {
            "content-type": "application/json",
            "Authorization": self.api_key,
        }
        response = requests.post(self.feedback_url, json=payload, headers=headers)
        self._check_response(response)

    def _record(
        self, log_id, input, output, latency, timestamp, date, custom_metric_values
    ) -> None:
        metadata = {
            "client_reported_metrics": {"latency": latency},
            "tags": {},
        }

        if self.session_id:
            metadata["tags"]["session_id"] = self.session_id

        payload = {
            "log_id": log_id,
            "model_name": self.model_name,
            "input": input,
            "output": output,
            "metadata": metadata,
            "timestamp": timestamp,
            "date": date,
            "custom_metric_values": custom_metric_values,
        }
        headers = {
            "content-type": "application/json",
            "Authorization": self.api_key,
        }
        response = requests.post(self.url, json=payload, headers=headers)
        self._check_response(response)

    def _handle_query(self, **input_kwargs):
        r"""
        Invoke the previously given LLM completion function with ``**kwargs``.
        Store the ``(input_kwargs, prompt)`` pair for another thread to process.
        The output of this method is the response from the LLM.

        Args:
            input_kwargs:  keyword arguments that are passed to the LLM for execution
        """
        try:
            start = perf_counter()
            response = self.completion_fn(**input_kwargs)
        except Exception:  # TODO: Coming soon, certain exceptions will be handled here
            raise

        log_id = str(uuid.uuid4())
        self._enqueue(
            TaskTypes.CREATE,
            (
                log_id,
                input_kwargs,
                response,
                perf_counter() - start,
                get_current_time_millis(),
                get_present_date(),
            ),
        )
        if self.track_feedback:
            response["hegel_id"] = log_id
        return response

    def __call__(self, **kwargs):
        r"""
        Invoke the previously given LLM completion function with ``**kwargs``.
        Store the ``(input_kwargs, prompt)`` pair for another thread to process.
        The output of this method is the response from the LLM.

        Args:
            input_kwargs:  keyword arguments that are passed to the LLM for execution
        """
        return self._handle_query(**kwargs)

    def add_feedback(self, log_id: str, feedback_data: Dict[str, object]):
        self._enqueue(
            TaskTypes.UPDATE,
            (log_id, feedback_data, get_current_time_millis(), get_present_date()),
        )

    def shutdown(self) -> None:
        r"""
        Stops the worker thread from executed and joins it.
        """
        self.data_queue.join()
        self.is_running = False
        self.worker_thread.join()

    def __del__(self) -> None:
        self.shutdown()


if __name__ == "__main__":
    r"""
    The following is an example of how `HegelScribe` works (without making a call to a remote LLM).
    """

    def mock_complete_fn(**kwargs):
        return {
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "The World Series in 2020 was played at Globe Life Field in Arlington, Texas.",
                        "role": "assistant",
                    },
                }
            ],
            "created": 1687839008,
            "id": "",
            "model": "gpt-3.5-turbo-0301",
            "object": "chat.completion",
            "usage": {"completion_tokens": 18, "prompt_tokens": 57, "total_tokens": 75},
        }

    scribe = HegelScribe(
        name="Helpful Assistant",
        session_id=HegelScribe.create_session_id(),
        track_feedback=True,
        completion_fn=mock_complete_fn,
    )
    response = scribe(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {
                "role": "assistant",
                "content": "The Los Angeles Dodgers won the World Series in 2020.",
            },
            {"role": "user", "content": "Where was it played?"},
        ],
    )
    scribe.add_feedback(response["hegel_id"], {"thumbs_up": True})
    scribe.add_feedback(response["hegel_id"], {"customer_succeeded": True})
    scribe.shutdown()
