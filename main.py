from flask import Flask, jsonify, request, Response
import datetime
import threading
import time

app = Flask(__name__)

# Task data store
tasks = [
    {'id': 1, 'title': 'Grocery Shopping', 'completed': False, 'due_date': '2024-03-15'},
    {'id': 2, 'title': 'Pay Bills', 'completed': False, 'due_date': '2024-03-20'},
]
next_task_id = 3

# In-memory list of SSE subscribers
subscribers = []

# --- Background notification function ---
def send_notification(task_id):
    time.sleep(2)  # Simulate email or push notification delay
    print(f"[Background] Notification sent for task {task_id}")
    notify_subscribers(f'{{"type": "TASK_UPDATED", "task_id": {task_id}}}')

# --- SSE Push ---
def notify_subscribers(message):
    for sub in subscribers:
        sub.append(message)

@app.route('/api/stream')
def stream():
    def event_stream():
        messages = []
        subscribers.append(messages)
        try:
            while True:
                while messages:
                    msg = messages.pop(0)
                    yield f"data: {msg}\n\n"
                time.sleep(1)
        except GeneratorExit:
            subscribers.remove(messages)
    return Response(event_stream(), mimetype="text/event-stream")

# --- REST API Endpoints ---

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    global next_task_id
    data = request.get_json()
    new_task = {
        'id': next_task_id,
        'title': data['title'],
        'completed': False,
        'due_date': data.get('due_date') or datetime.date.today().strftime("%Y-%m-%d")
    }
    next_task_id += 1
    tasks.append(new_task)
    notify_subscribers(f'{{"type": "TASK_CREATED", "task": {new_task}}}')
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task.update(data)
            threading.Thread(target=send_notification, args=(task_id,)).start()
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[i]
            notify_subscribers(f'{{"type": "TASK_DELETED", "task_id": {task_id}}}')
            return jsonify({'message': 'Task deleted'}), 204
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
