// task-updates.js
import { fromEvent } from 'rxjs';
import { map } from 'rxjs/operators';

// Create a connection to the Flask SSE endpoint
const eventSource = new EventSource('/api/stream');

// Wrap the 'message' event in an RxJS Observable
const taskUpdates$ = fromEvent(eventSource, 'message').pipe(
  map(event => JSON.parse(event.data))
);

// Subscribe to receive real-time task events
taskUpdates$.subscribe(update => {
  console.log('Real-time task update:', update);

  switch (update.type) {
    case 'TASK_UPDATED':
      console.log(`Task ${update.task_id} was updated.`);
      break;
    case 'TASK_CREATED':
      console.log('New task created:', update.task);
      break;
    case 'TASK_DELETED':
      console.log(`Task ${update.task_id} was deleted.`);
      break;
    default:
      console.log('Unknown event type:', update);
  }
});
