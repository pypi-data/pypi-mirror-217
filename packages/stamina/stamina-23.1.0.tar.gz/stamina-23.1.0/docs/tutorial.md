# Tutorial

## Retries?

Retries are essential for making distributed systems resilient.
Transient errors are unavoidable and can happen for the wildest reasons -- sometimes, one never finds out.

However, retries are also very dangerous if done naïvely.
Simply repeating an operation until it succeeds can lead to [*cascading failures*](https://en.wikipedia.org/wiki/Cascading_failure) and [*thundering herds*](https://en.wikipedia.org/wiki/Thundering_herd_problem) and ultimately take down your whole system, just because a database had a brief hiccup.

So:

1. You must wait between your retries: this is called a *backoff*.
2. You can't retry simultaneously with all your clients, so you must introduce randomness into your *backoff*: a *jitter*.
3. You must not retry forever.
   Sometimes a remote service is down indefinitely, and you must deal with it.

But how long should you back off?
The failure could be a network hiccup, so 100ms?
Maybe an application was just being deployed, so let's do 1 second?
But what if it's a database that's overloaded?
Then maybe 10 seconds?
And so forth.

The answer is:
You do all of those.
You start with a small backoff and increase it exponentially, adding a random *jitter*

That's what *stamina* does by default:
It starts with 100ms and increases exponentially by 2 until it reaches 45 seconds or 10 attempts.
A *jitter* between 0 and 1 second is added at every step.

That means the first backoff is no longer than 1.1 seconds, and the last is no longer than 46 seconds.
You can [tune all these parameters](stamina.retry) to your liking, but the defaults are a good starting point.

---

If you want to learn more:

- The [*Exponential Backoff And Jitter*](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) article on the *AWS Architecture Blog* is a good explanation of the basics with pretty graphs.
- [*Resiliency in Distributed Systems*](https://blog.pragmaticengineer.com/resiliency-in-distributed-systems/) takes a broader view and explains how to build resilient systems in general.
- And finally, I've given a talk at PyCon US 2017 called [*Solid Snakes or: How to Take 5 Weeks of Vacation*](https://www.youtube.com/watch?v=YVuqeXyvOUc) that addresses the various aspects to take care of to... take five weeks of (uninterrupted!) vacation.
  This one has a stronger focus on Python and working at a smaller scale.


## Decorators

The easiest way to add smart retries to your code is to decorate a callable with {func}`stamina.retry()`:

```python
import datetime as dt

import httpx

import stamina


@stamina.retry(on=httpx.HTTPError, attempts=3)
def do_it(code: int) -> httpx.Response:
    resp = httpx.get(f"https://httpbin.org/status/{code}")
    resp.raise_for_status()

    return resp

# reveal_type(do_it)
# note: Revealed type is "def (code: builtins.int) -> httpx._models.Response"
```

This will retry the function up to 3 times if it raises an {class}`httpx.HTTPError` (or any subclass thereof).
Since retrying on {class}`Exception` is an attractive nuisance, *stamina* doesn't do it by default and forces you to be explicit.

To give you observability of your application's retrying, *stamina* will count the retries using [*prometheus-client*](https://github.com/prometheus/client_python) in the `stamina_retries_total` counter and log them out using [*structlog*](https://www.structlog.org/), if they're installed.


## Arbitrary Code Blocks

Sometimes you only want to retry a part of a function.

Since iterators can't catch exceptions and context managers can't execute the same block multiple times, we need both to achieve that.
*stamina* gives you the {func}`stamina.retry_context()` iterator which yields the necessary context managers:

```python
for attempt in stamina.retry_context(on=httpx.HTTPError):
    with attempt:
        resp = httpx.get(f"https://httpbin.org/status/404")
        resp.raise_for_status()
```


## Async

Async works with the same functions and arguments -- you just have to use async functions and `async for`:

```python
@stamina.retry(
    on=httpx.HTTPError, attempts=3, timeout=dt.timedelta(seconds=10)
)
async def do_it_async(code: int) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://httpbin.org/status/{code}")
    resp.raise_for_status()

    return resp

# reveal_type(do_it_async)
# note: Revealed type is "def (code: builtins.int) -> typing.Coroutine[Any, Any, httpx._models.Response]"

async def with_block(code: int) -> httpx.Response:
    async for attempt in stamina.retry_context(on=httpx.HTTPError, attempts=3):
        with attempt:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"https://httpbin.org/status/{code}")
            resp.raise_for_status()

    return resp
```


## Deactivating Retries Globally

Occasionally it's handy to turn off retries globally -- for instance, in tests.
*stamina* has two helpers for controlling and inspecting whether retrying is active:
{func}`stamina.is_active()` and {func}`stamina.set_active()` (it's idempotent: you can call `set_active(True)` as many times as you want in a row).
For example, here's a *pytest* fixture that automatically turns off retries at the beginning of a test run:

```python
@pytest.fixture(autouse=True, scope="session")
def deactivate_retries():
    stamina.set_active(False)
```
