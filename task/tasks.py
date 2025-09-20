from celery import shared_task
from django.utils import timezone
from .models import Task

@shared_task(bind=True, max_retries=3)
def send_reminder(self, task_id):
    """
    This task runs when a Task is due. It updates is_reminded and
    performs notifications (email/websocket/etc).
    """
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return f"task {task_id} not found"

    if task.is_completed or task.is_reminded:
        return f"already handled {task_id}"

    # Do whatever notification you need:
    # - send email
    # - send websocket message via channels
    # - push notification
    # Example: mark as reminded
    task.is_reminded = True
    task.save(update_fields=["is_reminded"])
    # optionally return some value
    return f"reminder sent for task {task_id}"

@shared_task
def check_due_tasks():
    now = timezone.now()
    tasks = Task.objects.filter(due_time__lte=now, is_reminded=False, is_completed=False)
    for task in tasks:
        task.is_reminded = True
        task.save(update_fields=["is_reminded"])
        print(f"🔔 Reminder for task: {task.title}")