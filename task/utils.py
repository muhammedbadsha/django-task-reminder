# tasks/utils.py
import threading, time
from datetime import datetime
from django.utils.timezone import make_naive
from .models import Task

def reminder_thread(task_id, remind_at):
    """
    Runs in background until due_time, then updates is_reminded.
    """
    now = datetime.now().timestamp()
    remind_time = make_naive(remind_at).timestamp()  # convert aware -> naive
    wait_time = remind_time - now

    if wait_time > 0:
        time.sleep(wait_time)  # wait till due_time

    try:
        task = Task.objects.get(id=task_id)
        if not task.is_reminded and not task.is_completed:
            task.is_reminded = True
            task.save(update_fields=["is_reminded"])
            print(f"🔔 Reminder: {task.title} is due at {task.due_time}")
    except Task.DoesNotExist:
        pass


def start_reminder(task):
    """
    Helper to start reminder in a thread (non-blocking).
    """
    t = threading.Thread(target=reminder_thread, args=(task.id, task.due_time))
    t.daemon = True
    t.start()
