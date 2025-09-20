import threading, time
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer
from .utils import start_reminder, reminder_thread


# def reminder_thread(task_id, remind_at):
#     now = datetime.now().timestamp()
#     wait_time = remind_at.timestamp() - now
#     if wait_time > 0:
#         time.sleep(wait_time)  
    
    
#     from .models import Task
#     try:
#         task = Task.objects.get(id=task_id)
#         if not task.is_reminded and not task.is_completed:
#             print(f"Reminder: {task.title} (Due: {task.due_time})")
#             task.is_reminded = True
#             task.save()
#     except Task.DoesNotExist:
#         pass


class TaskListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(user=request.user)
            start_reminder(task) 
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Task.objects.get(pk=pk, user=user)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({"error": "Task not found"}, status=404)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({"error": "Task not found"}, status=404)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            task = serializer.save()

            # restart reminder if due_time changed
            if "due_time" in request.data:
                t = threading.Thread(target=reminder_thread, args=(task.id, task.due_time))
                t.daemon = True
                t.start()

            return Response(TaskSerializer(task).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({"error": "Task not found"}, status=404)
        task.delete()
        return Response({"msg": "Task deleted"}, status=204)
