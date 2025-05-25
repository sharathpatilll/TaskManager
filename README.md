# TaskManager

1. Explanation of Changes (Asynchronous Notifications)
   
Problem:
In the original code, time.sleep(2) simulates notification sending synchronously, which blocks the main Flask thread, causing slow responses.

Solution:
- Used Python's threading.Thread to offload the simulated notification to a background thread.
- This allows Flask to immediately return the HTTP response while the notification is handled in the background.

Benefits:
- Improves API responsiveness and scalability.
- Avoids blocking the main thread during slow operations like email/SMS sending.


2. RxJS Integration Design Using Event Streams

Goal:
Push task updates (e.g., task modified, created, or deleted) from backend to frontend in real-time, where RxJS can consume and react to the changes.

In the Frontend:
- Used RxJS fromEvent to listen to SSE/WebSocket messages.
- Stream updates into observables, enabling transformation and composition.

Using RxJS instead of just onmessage gives you:
- Composability: You can filter, debounce, merge, throttle, etc.
- Reactive Architecture: Integrates with other reactive streams like user input, form changes, etc.
- Error Handling & Retry: Can retry failed connections or transform streams easily.
- Testability: Observables are easier to mock/test than imperative callbacks.
