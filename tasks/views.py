from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response
from justtwotasks.tasks.models import Task

def main(request):
    max_tasks = 2
    if request.method == 'POST':
        if 'tasks[]' in request.POST:
            tasks = request.POST.getlist('tasks[]')
            if 'task_ids[]' in request.POST:
                task_ids = request.POST.getlist('task_ids[]')

            # Ensure we only have no more than the max tasks processed
            tasks = tasks[:max_tasks]

            for i in enumerate(tasks):
                key = i[0]
                # If we've set the key, we're updating an existing task
                if int(task_ids[key]):
                    task = Task.objects.get(pk=int(task_ids[key]))
                    task.task = tasks[key]
                    task.save()
                # Otherwise, it's brand new
                else:
                    Task.objects.create(task=tasks[key], is_complete=False)

    task_to_edit = None;
    if request.method == 'GET':
        if 'edit_task' in request.GET:
            task_to_edit = int(request.GET['edit_task'])
        elif 'delete_task' in request.GET:
            task = Task.objects.get(pk=int(request.GET['delete_task']))
            task.delete()
        elif 'complete_task' in request.GET:
            task = Task.objects.get(pk=int(request.GET['complete_task']))
            if task.is_complete:
                task.is_complete = False
            else:
                task.is_complete = True
            task.save()

    # Get all of today's tasks
    tasks = Task.objects.all().order_by('id')
    tasks_to_create = range(1, (max_tasks - len(list(tasks)))+1)

    args = {'tasks':tasks,
            'task_to_edit':task_to_edit,
            'tasks_to_create':tasks_to_create}

    return render_to_response('tasks.html', 
                              args,
                              context_instance=RequestContext(request))

