"""Event Manager"""

import atexit
from typing import Callable, TypeAlias
from queue import Queue
from threading import Event, Lock, Thread

from .log import info

EventCallback: TypeAlias = Callable[[], bool | None]


class EventManager:
    """EventManager"""

    def __init__(self, name: str = ""):
        self._name = name or str(id(self))
        self._registry: dict[str, list[EventCallback]] = {}
        self._lock = Lock()
        self._stop = Event()
        self._queue = Queue()
        self._thread = Thread(target=self._run, name=f"EventThread-{self._name}")
        self._thread.daemon = True
        self._thread.start()

        @atexit.register
        def finalizer():
            self.shutdown()

    def register(self, event: str):
        """Register an event"""

        def inner(func: EventCallback):
            with self._lock:
                self._registry.setdefault(event, [])
                info("Registering %s under %s", repr(func), event)
                if self._registry[event]:
                    self._registry[event].append(func)
                else:
                    self._registry[event] = [func]
                return func

        return inner

    def dispatch(self, event: str):
        """Dispatch an event"""
        info("Dispatching %s", event)
        self._queue.put(event)

    def _run(self):
        """Run the event manager in separate thread"""
        while not self._stop.is_set():
            event = self._queue.get()
            info("Fetching event %s", event)
            with self._lock:
                handlers = self._registry.get(event, [])
            for handler in handlers:
                info("Executing %s under %s", repr(handler), event)
                ret = handler()
                if ret:  # Return early when an event aborts event lineup
                    break
            self._queue.task_done()

    def shutdown(self):
        """Shutdown the event manager"""
        self._stop.set()
        self._thread.join()
        info("Event manager %s has been shut down", self._name)

GLOBAL = EventManager("GlobalEvent")

register = GLOBAL.register
dispatch = GLOBAL.dispatch

__all__ = ["EventManager", "EventCallback", "GLOBAL", "register", "dispatch"]
