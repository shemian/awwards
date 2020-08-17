from django.test import TestCase
from .models import *


# Create your tests here.
class  ProfileModelTests(TestCase):
    """
    class facilitates the creation of test units to test profile model's behavior
    """
    def setUp(self):
        """
        method defines the instructions to be executed before each test
        """
        self.new_user = User(username="wendo", email="wendo11@gmail.com", password="qwerty")
        self.new_user.save()
        self.new_profile = Profile(bio="anything crazy", user=self.new_user, profile_pic="mypic.jpg")
    
    def test_instance(self):
        """
        method checks model's object are initialization
        """
        self.assertTrue(isinstance(self.new_profile, Profile))

    def test_save_profile(self):
        """
        test unit tests if the model's object are saved to the database
        """
        self.new_profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)
    
    def test_update_profile(self):
        """
        method  update profile function
        """
        self.new_profile.save_profile()
        Profile.objects.filter(pk=self.new_profile.pk).update(bio="update smthg")
        self.new_profile.update_profile()
        self.assertEqual(self.new_profile.bio, 'update smthg')
    
    def test_delete_profile(self):
        """
        method  delete function
        """
        self.new_profile.save_profile()
        Profile.objects.filter(pk=self.new_profile.pk).delete()
        self.new_profile.delete_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) == 0)

class ProjectsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='test')
        self.projects = Projects.objects.create(id=1,project_name='test post', project_image='https://ucarecdn.com/0ccf61ff-508e-46c6-b713-db51daa6626e', description='desc',
                                        project_user=self.user, url='http://usbbfbr.com',github_repo='https://github.com/OwinoLucas/akan')

    def test_instance(self):
        """
        method checks if objects are initialized properly
        """
        self.assertTrue(isinstance(self.projects, Projects))

    def test_save_post(self):
        """
        method tests if an added post objects is saved to the database
        """
        self.image.save_projects()
        projects = Post.objects.all()
        self.assertTrue(len(posts) > 0)
    
    def test_update_projects(self):
        """
        method test if a saved post object can be updated
        """
        self.projects_image.save_post()
        Post.objects.filter(pk=self.image.pk).update(image_name="random")
        self.projects_image.update_post()
        self.assertEqual(self.projects_image.projects_name, 'random')

    def test_delete_projects(self):
        """
        method check if a saved post objects can be deleted
        """
        self.projects_image.save_postprojects()
        Post.objects.filter(pk=self.projects_image.pk).delete()
        self.image.delete_post()
        projects = Post.objects.all()
        self.assertTrue(len(posts) == 0)
    
        
    def test_get_projects(self):
        self.project.save()
        project = Projects.all_projects()
        self.assertTrue(len(project) > 0)