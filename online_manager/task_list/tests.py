from django.test import TestCase, RequestFactory

from task_list.views import FilteredTasks
from task_list.task_crud import TaskCrud
from task_list.models import Task, User


class TaskFilterTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('test_user1', password='test_password')
        self.user1.save()
        user2 = User.objects.create_user('test_user2', password='test_password')
        user2.save()

        Task(name='Test task 1', owner=self.user1, is_done=False).save()
        Task(name='Test task 2', owner=self.user1, is_done=False).save()
        Task(name='Test task 3', owner=self.user1, is_done=True, marked_done_by=self.user1).save()

        Task(name='Test task 1a', owner=user2, is_done=False).save()
        Task(name='Test task 2b', owner=user2, is_done=False).save()

    def test_own_tasks_filter(self):
        filtered_tasks = FilteredTasks(self.user1)

        result = filtered_tasks.to_dict()
        assert len(result['my_tasks']) is 3

    def test_others_tasks_filter(self):
        filtered_tasks = FilteredTasks(self.user1)

        result = filtered_tasks.to_dict()
        assert len(result['others_tasks']) is 2

    def tearDown(self):
        pass


class TaskCrudTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.task = Task(name='Test task', owner=self.user, is_done=False)
        self.task.save()
        self.done_task = Task(name='Test done task', owner=self.user, is_done=True, marked_done_by=self.user)
        self.done_task.save()

    def test_create_method(self):
        data = {'task_name': 'new_task_name'}
        kwargs = {'method': 'create'}
        request = self.factory.post(path='/task_crud/create/', data=data, )
        request.user = self.user
        response = TaskCrud.as_view()(request, **kwargs)

        created_task = Task.objects.filter(owner=self.user, name=data['task_name'])
        assert len(created_task) is 1

    def test_edit(self):
        data = {'task_id': self.task.id, 'task_name': 'new_task_name'}
        kwargs = {'method': 'edit'}
        request = self.factory.post(path='/task_crud/edit/', data=data, )
        request.user = self.user
        response = TaskCrud.as_view()(request, **kwargs)

        modified_task = Task.objects.get(id=self.task.id)
        assert modified_task.name == data['task_name']

    def test_delete_method(self):
        task_id = self.task.id
        data = {'task_id': task_id}
        kwargs = {'method': 'delete'}
        request = self.factory.post(path='/task_crud/delete/', data=data, )
        request.user = self.user
        response = TaskCrud.as_view()(request, **kwargs)

        deleted_task = Task.objects.filter(id=task_id)
        assert len(deleted_task) is 0

    def test_mark_done(self):
        data = {'task_id': self.task.id}
        kwargs = {'method': 'done'}
        request = self.factory.post(path='/task_crud/done/', data=data, )
        request.user = self.user
        response = TaskCrud.as_view()(request, **kwargs)

        modified_task = Task.objects.get(id=self.task.id)
        assert modified_task.is_done is True
        assert modified_task.marked_done_by.username == self.user.username

    def test_mark_undone(self):
        data = {'task_id': self.done_task.id}
        kwargs = {'method': 'undone'}
        request = self.factory.post(path='/task_crud/undone/', data=data, )
        request.user = self.user
        response = TaskCrud.as_view()(request, **kwargs)

        modified_task = Task.objects.get(id=self.done_task.id)
        assert modified_task.is_done is False
        assert modified_task.marked_done_by is None

    def tearDown(self):
        pass