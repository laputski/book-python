import contextvars, logging, uuid
from contextlib import contextmanager

request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")

@contextmanager
def request_scope(value: str | None = None):
    token = request_id.set(value or uuid.uuid4().hex)
    try:
        yield request_id.get()
    finally:
        request_id.reset(token)          # возврат прежнего значения

class RequestFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id.get()
        return True
