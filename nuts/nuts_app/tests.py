from django.test import TestCase, Client
from nuts_app.models import *
from django.contrib.auth.models import User
import datetime
# Create your tests here.

class NutModelsTest(TestCase):
    def test_simple_add(self):
        self.assertTrue(Nut.objects.all().count() == 0)
        new_user = User(username='hhh')
        new_user.save()
        new_nut = Nut(author=new_user, title='test', description='describe test', privilege='Public',expire_time= datetime.datetime.now())
        new_nut.save()
        self.assertTrue(Nut.objects.all().count() == 1)
        self.assertTrue(Nut.objects.filter(author=new_user))
        self.assertTrue(Nut.objects.filter(title__contains='test'))
        self.assertTrue(Nut.objects.filter(description__contains='describe'))  
        self.assertTrue(Nut.objects.filter(privilege='Public'))  
        self.assertTrue(Nut.objects.filter(expire_time=datetime.datetime.now()))
        self.assertTrue(Nut.objects.filter(state='TODO'))
    
    def test_retrieve_by_user(self):
        self.assertTrue(Nut.objects.all().count() == 0)
        new_user = User(username='h2')
        new_user.save()
        new_nut = Nut(author=new_user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_user = User(username='hhh')
        new_user.save()
        new_nut = Nut(author=new_user, title='test', description='describe test', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test2', description='describe test2', privilege='Private',expire_time = datetime.datetime.now())
        new_nut.save()
        self.assertTrue(Nut.objects.all().count() == 3)
        self.assertTrue(Nut.objects.filter(author=new_user).all().count() == 2)
        
    def test_retrieve_public(self):
        self.assertTrue(Nut.objects.all().count() == 0)
        new_user = User(username='h2')
        new_user.save()
        new_nut = Nut(author=new_user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_user = User(username='hhh')
        new_user.save()
        new_nut = Nut(author=new_user, title='test', description='describe test', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test2', description='describe test2', privilege='Private',expire_time = datetime.datetime.now())
        new_nut.save()
        self.assertTrue(Nut.objects.all().count() == 3)
        self.assertTrue(Nut.objects.filter(privilege='Public').all().count() == 2)
        
    def test_retrieve_private(self):
        self.assertTrue(Nut.objects.all().count() == 0)
        new_user = User(username='h2')
        new_user.save()
        new_nut = Nut(author=new_user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_user = User(username='hhh')
        new_user.save()
        new_nut = Nut(author=new_user, title='test', description='describe test', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test2', description='describe test2', privilege='Private',expire_time = datetime.datetime.now())
        new_nut.save()
        self.assertTrue(Nut.objects.all().count() == 3)
        self.assertTrue(Nut.objects.filter(privilege='Private').all().count() == 1)
        
    def test_retrieve_todo(self):
        self.assertTrue(Nut.objects.all().count() == 0)
        new_user = User(username='h2')
        new_user.save()
        new_nut = Nut(author=new_user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test', description='describe test', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test2', description='describe test2', privilege='Private',expire_time = datetime.datetime.now())
        new_nut.save()
        self.assertTrue(Nut.objects.all().count() == 3)
        self.assertTrue(Nut.get_todo(user=new_user).count() == 3)
        new_nut.state = 'DONE'
        new_nut.save()
        self.assertTrue(Nut.get_todo(user=new_user).count() == 2)
        
    def test_retrieve_doing(self):
        self.assertTrue(Nut.objects.all().count() == 0)
        new_user = User(username='h2')
        new_user.save()
        new_nut = Nut(author=new_user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test', description='describe test', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test2', description='describe test2', privilege='Private',expire_time = datetime.datetime.now())
        new_nut.save()
        self.assertTrue(Nut.objects.all().count() == 3)
        self.assertTrue(Nut.get_doing(user=new_user).count() == 0)
        new_nut.state = 'DOING'
        new_nut.save()
        self.assertTrue(Nut.get_doing(user=new_user).count() == 1)
        
    def test_retrieve_done(self):
        self.assertTrue(Nut.objects.all().count() == 0)
        new_user = User(username='h2')
        new_user.save()
        new_nut = Nut(author=new_user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test', description='describe test', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test2', description='describe test2', privilege='Private',expire_time = datetime.datetime.now())
        new_nut.save()
        self.assertTrue(Nut.objects.all().count() == 3)
        self.assertTrue(Nut.get_done(user=new_user).count() == 0)
        new_nut.state = 'DONE'
        new_nut.save()
        self.assertTrue(Nut.get_done(user=new_user).count() == 1)
        
    def test_retrieve_all(self):
        self.assertTrue(Nut.objects.all().count() == 0)
        new_user = User(username='h2')
        new_user.save()
        new_nut = Nut(author=new_user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test', description='describe test', privilege='Public',expire_time = datetime.datetime.now())
        new_nut.save()
        new_nut = Nut(author=new_user, title='test2', description='describe test2', privilege='Private',expire_time = datetime.datetime.now())
        new_nut.save()
        self.assertTrue(Nut.objects.all().count() == 3)
        self.assertTrue(Nut.get_all(user=new_user).count() == 3)
        new_nut.state = 'DONE'
        new_nut.save()
        self.assertTrue(Nut.get_all(user=new_user).count() == 3)

class SquirrelModelsTest(TestCase):
    def test_simple_add(self):
        self.assertTrue(Squirrel.objects.all().count() == 0)
        new_user1 = User(username='hhh')
        new_user1.save()
        new_squirrel1 = Squirrel(user=new_user1, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()
        self.assertTrue(Squirrel.objects.all().count() == 1)
        self.assertTrue(Squirrel.objects.filter(user=new_user1))
        self.assertTrue(Squirrel.objects.filter(age=5))
        self.assertTrue(Squirrel.objects.filter(location='pittsburgh'))  
        self.assertTrue(Squirrel.objects.filter(description__contains='describe'))  
    
    def test_follow_user(self):
        self.assertTrue(Squirrel.objects.all().count() == 0)
        new_user1 = User(username='hhh')
        new_user1.save()
        new_squirrel1 = Squirrel(user=new_user1, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()       
        new_user2 = User(username='hhh2')
        new_user2.save()
        new_squirrel2 = Squirrel(user=new_user2, age=5, location='pittsburgh', description='describe squirrel2')
        new_squirrel2.save()
        new_squirrel2.follow_user.add(new_squirrel1)
        new_squirrel2.save()       
        self.assertTrue(Squirrel.objects.all().count() == 2)
        self.assertTrue(Squirrel.objects.get(user=new_user2).follow_user.all().count() == 1)
        self.assertTrue(Squirrel.objects.get(user=new_user2).follow_user.filter(user=new_user1))
        self.assertFalse(Squirrel.objects.get(user=new_user1).follow_user.filter(user=new_user2))
    
    def test_follow_plan(self):
        self.assertTrue(Squirrel.objects.all().count() == 0)
        new_user1 = User(username='hhh')
        new_user1.save()
        new_squirrel1 = Squirrel(user=new_user1, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=new_user1, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()    
        new_user2 = User(username='hhh2')
        new_user2.save()
        new_squirrel2 = Squirrel(user=new_user2, age=5, location='pittsburgh', description='describe squirrel2')
        new_squirrel2.save()
        new_squirrel2.follow_plan.add(new_nut1)
        new_squirrel2.save()  
        new_nut2 = Nut(author=new_user2, title='test2', description='describe test2', privilege='Public',expire_time = datetime.datetime.now())
        new_nut2.save()    
        self.assertTrue(Squirrel.objects.all().count() == 2)
        self.assertTrue(Squirrel.objects.get(user=new_user2).follow_plan.all().count() == 1) 
        self.assertTrue(Squirrel.objects.get(user=new_user2).follow_plan.filter(title='test3'))
        self.assertFalse(Squirrel.objects.get(user=new_user2).follow_plan.filter(title='test2'))

class CommentModelTest(TestCase):
    def test_add_comment(self):
        self.assertTrue(Comment.objects.all().count() == 0)
        new_user1 = User(username='hhh')
        new_user1.save()
        new_user2 = User(username='hhh2')
        new_user2.save()
        new_nut1 = Nut(author=new_user1, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        new_comment = Comment(nut=new_nut1, text='hello', user=new_user2)
        new_comment.save()
        self.assertTrue(Comment.objects.all().count() == 1)
        self.assertTrue(Comment.objects.filter(nut=new_nut1).count() == 1)
        self.assertTrue(Comment.objects.filter(text='hello').count() == 1)
        self.assertTrue(Comment.objects.filter(user=new_user2).count() == 1)
    
    def test_log_get_nut_comment(self):
        self.assertTrue(Comment.objects.all().count() == 0)
        new_user1 = User(username='hhh')
        new_user1.save()
        new_user2 = User(username='hhh2')
        new_user2.save()
        new_nut1 = Nut(author=new_user1, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        new_comment = Comment(nut=new_nut1, text='hello', user=new_user2)
        new_comment.save()
        new_comment = Comment(nut=new_nut1, text='hello again', user=new_user2)
        new_comment.save()
        self.assertTrue(Comment.objects.filter(nut=new_nut1).count() == 2)
        
class MessageModelTest(TestCase):
    def test_add_message(self):
        self.assertTrue(Message.objects.all().count() == 0)
        new_message = Message(message='title', room_id='1_3')
        new_message.save()
        self.assertTrue(Message.objects.all().count() == 1)
    
    def test_get_message_by_room(self):
        self.assertTrue(Message.objects.all().count() == 0)
        new_message = Message(message='title', room_id='1_3')
        new_message.save()
        new_message = Message(message='title1', room_id='1_3')
        new_message.save()
        new_message = Message(message='title3', room_id='1_2')
        new_message.save()
        self.assertTrue(Message.objects.filter(room_id='1_3').count() == 2)
        
class NutTest(TestCase):
    def test_nonlog_home_page(self):   # Tests that a GET request to /nuts/home
        client = Client()      
        response = client.get('/nuts/home')
        self.assertEqual(response.status_code, 302)
    
    def test_login_page(self):   # Tests that a POST request to /nuts/login
        new_user1 = User(username='fred', password='secret')
        new_user1.save()
        client = Client()       # results in an HTTP 200 (OK) response.
        response = client.post('/nuts/login', {'username': 'fred', 'password': 'secret'})
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):   # Tests that could log in
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)
    
    def test_log_home_page(self):   # Tests that a GET request to /nuts/
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/')
        self.assertEqual(response.status_code, 200)
        
    def test_log_profile(self):   # Tests that a GET request to /nuts/show-profile/1/
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/show-profile/1/')
        self.assertEqual(response.status_code, 404)
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()
        response = client.get('/nuts/show-profile/1/')
        self.assertEqual(response.status_code, 200)
     
    def test_log_morenuts_page(self):   # Tests that a GET request to /nuts/more-nuts/
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/more-nuts/')
        self.assertEqual(response.status_code, 200)
    
    def test_log_allpublic_page(self):   # Tests that a GET request to /nuts/get_all_public/
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()    
        new_user2 = User(username='hhh2')
        new_user2.save()
        new_squirrel2 = Squirrel(user=new_user2, age=5, location='pittsburgh', description='describe squirrel2')
        new_squirrel2.save()
        new_nut2 = Nut(author=new_user2, title='test2', description='describe test2', privilege='Public',expire_time = datetime.datetime.now())
        new_nut2.save()    
        new_squirrel1.follow_plan.add(new_nut2)
        new_squirrel1.save()  
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/get_all_public/')
        self.assertTrue(response.json()['nuts'])
    
    def test_log_alleat_page(self):   # Tests that a GET request to /nuts/get_all_eat/
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()    
        new_user2 = User(username='hhh2')
        new_user2.save()
        new_squirrel2 = Squirrel(user=new_user2, age=5, location='pittsburgh', description='describe squirrel2')
        new_squirrel2.save()
        new_nut2 = Nut(author=new_user2, title='test2', description='describe test2', privilege='Public',expire_time = datetime.datetime.now())
        new_nut2.save()    
        new_squirrel1.follow_plan.add(new_nut2)
        new_squirrel1.save()  
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/get_all_eat/')
        self.assertTrue(response.json()['nuts'])
        
    def test_log_allfollow_page(self):   # Tests that a GET request to /nuts/get_all_follow/
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()    
        new_user2 = User(username='hhh2')
        new_user2.save()
        new_squirrel2 = Squirrel(user=new_user2, age=5, location='pittsburgh', description='describe squirrel2')
        new_squirrel2.save()
        new_nut2 = Nut(author=new_user2, title='test2', description='describe test2', privilege='Public',expire_time = datetime.datetime.now())
        new_nut2.save()    
        new_squirrel1.follow_user.add(new_squirrel2)
        new_squirrel1.save()  
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/get_all_follow/')
        self.assertTrue(response.json()['nuts'])
        
    def test_log_viewplan_page(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/view-plan/1')
        self.assertEqual(response.status_code, 200)
        
    def test_log_search(self):   # Tests that a GET request to /nuts/search-plan
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/search-plan')
        self.assertEqual(response.status_code, 200)
        
    def test_log_edit_profile(self):   # Tests that a POST request to /nuts/edit-profile
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.post('/nuts/edit-profile', {'location': 'New York'})
        self.assertEqual(response.status_code, 200)
    
    def test_log_show_edit_profile(self):   # Tests that a GET request to /nuts/edit-profile
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/edit-profile')
        self.assertEqual(response.status_code, 200)
        
    def test_log_photo(self):   # Tests that a GET request to /nuts/edit-profile
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel', image="default_image.jpg")
        new_squirrel1.save()   
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/photo/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        
    def test_log_show_create_plan(self):   # Tests that a GET request to /nuts/edit-profile
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/create-plan')
        self.assertEqual(response.status_code, 200)
        
    def test_log_create_plan(self):   # Tests that a GET request to /nuts/edit-profile
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.post('/nuts/create-plan', {'title': 'title', 'description': 'description', 
                                                     'start_time': timezone.now, 'expire_time': timezone.now, 'privilege': 'Public'})
        self.assertEqual(response.status_code, 200)
    
    def test_log_my_plan(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/my-plan')
        self.assertEqual(response.status_code, 200)
        
    def test_log_all_plan(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/view-all-plan')
        self.assertTrue(response.json()['nuts'])
        
    def test_log_edit_plan(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/edit-plan/1')
        self.assertEqual(response.status_code, 200)
        
    def test_log_edit_plan_do(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.post('/nuts/edit-plan/1', {'title':'ggg'})
        self.assertEqual(response.status_code, 200)
        
    def test_log_delete_plan(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/delete-plan/1')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Nut.objects.all().count() == 0)
        
    def test_log_udpate_state(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.post('/nuts/update-state/1', {'state':'DONE', 'point':'0'})
        self.assertEqual(response.status_code, 200)
        
    def test_log_eat_plan(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        user = User.objects.create(username='testuser1')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/eat_plan/True/1')
        self.assertEqual(response.status_code, 200)
        
    def test_log_like_plan(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        user = User.objects.create(username='testuser1')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/like_plan/True/1')
        self.assertEqual(response.status_code, 200)
        
    def test_log_follow_user(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        user = User.objects.create(username='testuser1')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/follow_user/True/2')
        self.assertEqual(response.status_code, 200)
        
    def test_log_all_mine(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        new_nut1 = Nut(author=user, title='test3', description='describe test3', privilege='Public',expire_time = datetime.datetime.now())
        new_nut1.save()
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.get('/nuts/view_all_mine')
        self.assertTrue(response.json()[0])
        
    def test_log_create_range(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.post('/nuts/create_range_plan', {'start_time': timezone.now, 'expire_time': timezone.now})
        self.assertEqual(response.status_code, 200)
        
    def test_log_edit_range(self):   # Tests that a GET request to /nuts/view-plan/1
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        new_squirrel1 = Squirrel(user=user, age=5, location='pittsburgh', description='describe squirrel')
        new_squirrel1.save()   
        
        client = Client()
        logged_in = client.login(username='testuser', password='12345')
        response = client.post('/nuts/edit-plan-time', {'start_time': timezone.now, 'expire_time': timezone.now})
        self.assertEqual(response.status_code, 200)