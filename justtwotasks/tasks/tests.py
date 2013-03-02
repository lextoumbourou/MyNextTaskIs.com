"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import datetime
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from justtwotasks.tasks.models import Task


class TasksTest(TestCase):
    def test_delete_task(self):
        """
        Test that a task deletes successfully after creating it
        """
        # Add a task to be deleted
        user = User.objects.create_user('test1', 'test@test.com', 'nopass')
        user.save()
        t = Task.objects.create(
            user=user, task="Test task", created=datetime.today(), is_complete=False)
        c = Client()
        response = c.delete('/task/{0}'.format(t.pk))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=t.pk))
