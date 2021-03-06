"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django.core import serializers
from django.contrib.auth.models import User

from mynexttaskis.tasks.models import Task, Category
from mynexttaskis.tasks import utils


class TasksTest(TestCase):
    def setUp(self):
        # Add a task to be deleted
        self.user = User.objects.create_user(
            'test1', 'test@test.com', 'nopass')
        self.user.save()

        self.client = Client()
        self.client.login(username='test1', password='nopass')

    def tearDown(self):
        self.client.logout()

    def test_delete_task(self):
        """Test that a task deletes successfully after creating it"""
        t = Task.objects.create(
            user=self.user, task='Test task', 
            created=datetime.today(), is_complete=False)

        # Test that delete fails for wrong user
        local_client = Client()
        response = local_client.delete('/api/task/{0}'.format(t.pk))
        self.assertEqual(response.status_code, 401)

        response = self.client.delete('/api/task/{0}'.format(t.pk))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=t.pk))


    def test_get_all_tasks(self):
        """Test that all tasks are returned"""
        t = Task.objects.create(
                user=self.user, task='Test task', 
                created=datetime.today(), is_complete=False)
        response = self.client.get('/api/task/')
        tasks = Task.objects.filter(
            user=self.user, 
            created=datetime.today()).order_by('is_complete', 'id')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content, serializers.serialize('json', tasks))

    def test_get_playing_task(self):
        """Get playing task"""
        t = Task.objects.create(
                user=self.user, task='Test task', 
                created=datetime.today(), is_complete=False, is_in_progress=True)
        response = self.client.get('/api/task/playing')
        task = Task.objects.filter(
            user=self.user, is_complete=False, is_in_progress=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content, serializers.serialize('json', task))


    def test_update_a_task(self):
        """Test that a task updates successfully"""
        t = Task.objects.create(
                user=self.user, task='Test task',
                created=datetime.today(), is_complete=False)
        data = json.dumps({"is_complete":True})
        # Test that delete fails for wrong user
        local_client = Client()
        response = local_client.post(
            '/api/task/{0}'.format(t.pk), data=data, 
            content_type='application/json')
        self.assertEqual(response.status_code, 401)

        response = self.client.post(
            '/api/task/{0}'.format(t.pk), data=data, 
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.get(pk=t.pk).is_complete, True) 


    def test_create_new_task(self):
        """Test that new task is created successfully"""
        task_name = 'Another test task'
        data = json.dumps({'task': task_name, 'is_complete': False})
        response = self.client.post(
            '/api/task/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)[0]['fields']['task'], task_name)

    def test_get_categories(self):
        """Test that a task is separate from its categories"""
        task_string = "This is the task #Test1 #Test2"
        result = ["Test1", "Test2"]
        self.assertEqual(utils.get_categories(task_string), result)

    def test_get_tasks_by_category(self):
        task_name = 'test Task 2'
        category, created = Category.objects.get_or_create(name="Test")
        t = Task.objects.create(
            user=self.user, task=task_name,
            created=datetime.today(), is_complete=False)
        t.save()
        t.categories.add(category)

        response = self.client.get(
                '/api/task/category?categories=Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)[0]['fields']['task'], task_name)
