import sentry_sdk



sentry_sdk.init(
    dsn="https://1e2ed7f2a97d4729957cdb965f804d6b@o4504231228145664.ingest.sentry.io/4504231271137280",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

# division_by_zero = 1 / 0

class MyException(Exception):
    pass

try:
    raise MyException("My hovercraft is full of eels")
except Exception as exc:
    sentry_sdk.capture_exception(exc)