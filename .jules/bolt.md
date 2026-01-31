## 2026-01-31 - Unblocking the Cortex
**Learning:** Even in `asyncio` applications, legacy synchronous clients (like `httpx.Client` or `requests`) can silently block the event loop, killing performance.
**Action:** Always wrap synchronous blocking calls in `asyncio.to_thread()` when working within an `async def` function, especially for IO-bound tasks like API calls.
