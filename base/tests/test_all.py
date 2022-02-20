from PIL import Image
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from base.models import Users, Comment, Subject, Classroom


#python manage.py test base/tests

class TestModel_Api(TestCase):

    def setUp(self):
        self.user_1 = Users.objects.create(name='user_name_1', password='user_password_1')
        self.user_2 = Users.objects.create(name='user_name_2', password='user_password_2')
        self.user_3 = Users.objects.create(name='user_name_3', password='user_password_3')

        self.subject_1 = Subject.objects.create(name='subject_1', is_tech=True)

        self.classroom_1=Classroom.objects.create(name='classroom_1',description='d_1',
                                             subject=self.subject_1, teacher=self.user_1)
        self.classroom_1.save()
        self.classroom_1.students.add(self.user_2,self.user_3)

        self.comment_1=Comment.objects.create(sender=self.user_2,classroom=self.classroom_1,
                                              text='message_1')


    def test_user_model(self):
        user_1=self.user_1
        self.assertTrue(isinstance(user_1, Users))
        self.assertEqual(user_1.slug, slugify(user_1.name))
        img = Image.open(user_1.picture.path)
        self.assertFalse(img.width>800 and img.height>900)

    def test_classroom_model(self):
        self.assertIn(self.user_2, self.classroom_1.students.all())
        self.assertEqual(2, self.classroom_1.students.count())

    def test_api_classrooms(self):
       user_2 = self.user_2
       url_2 = reverse('api_cls')
       #self.client.force_login(user_2)
       response_2 = self.client.get(url_2)
       self.assertEqual(response_2.status_code,200)

    def test_api_classroom(self):
       url_1=reverse('api_cl',args=[self.classroom_1.slug])
       response_1 = self.client.get(url_1)
       self.assertEqual(response_1.status_code,200)








