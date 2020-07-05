<<<<<<< HEAD
from django.contrib.auth.models import User 
from django.core.paginator import Paginator 
from django.shortcuts import reverse 
from django.test import TestCase 
from django.test import Client 
from .models import Post, Group 


def method(self):
    urls = ( 
            ('index', {}), 
            ('profile', {'username': self.user.username}), 
            ('post', {'username': self.user.username, 'post_id': self.post.id}) 
        ) 
    for name, kwargs in urls:
        response = self.client.get(reverse(name, kwargs=kwargs))
        paginator = response.context.get('paginator')
        if paginator is not None:
            post = response.context['page'][0]
        else:
            post = response.context['post']
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)


class TestMethods(TestCase): 
    def setUp(self): 
        self.client = Client() 
        self.user = User.objects.create_user( 
                        username="User",  
                        email="User@skynet.com",  
                        password="User" 
                        ) 
        self.group = Group.objects.create( 
                        slug="test4posts",  
                        title="Test Group", 
                        description="Test Descr." 
                        ) 
        self.post = Post.objects.create( 
            text="А теперь ты приходишь и говоришь: "+
            "Дон Корлеоне, мне нужна справедливость."+
            "Но ты не просишь с уважением, не предлагаешь дружбу, "+
            "даже не думаешь обратиться ко мне — крёстный.",  
            author=self.user, 
            group = self.group
            ) 

    def test_profile(self): 
=======
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import reverse
from django.test import TestCase
from django.test import Client
from .models import Post, Group


class TestMethods(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="User", 
                            email="User@skynet.com", 
                                password="User"
                                )
        self.group = Group.objects.create(
                        slug="test4posts", 
                            title="Test Group",
                                description="Test Descr."
                                )
        self.post = Post.objects.create(
            text=f"А теперь ты приходишь и говоришь: "
            f"Дон Корлеоне, мне нужна справедливость." 
            f"Но ты не просишь с уважением, не предлагаешь дружбу, "
            f"даже не думаешь обратиться ко мне — крёстный.", 
                author=self.user,
                    group = self.group)
        
    def test_Profile(self):
>>>>>>> 3f014c9be953bb38f7ee8faa4479f346c5d6f1b5
        """Проверка создания персональной страницы после регистрации"""
        response = self.client.get("/User/") 
        self.assertEqual(response.status_code, 200, msg='Страница не создана') 

    def test_authpost(self): 
        """Возможность публикации авторизованным пользователем"""
<<<<<<< HEAD
        entrance = self.client.force_login(self.user)
        response = self.client.post('/new/', {'text': 'text', 'group': 'Test Group'}, follow=True)
=======
        #post_url = reverse('post', args=(self.post.author, self.post.id,))
        #response = self.client.get(post_url)
        response = self.client.get("/new/", follow=True)
>>>>>>> 3f014c9be953bb38f7ee8faa4479f346c5d6f1b5
        self.assertEqual(response.status_code, 200, msg='Публикация невозможна')

    def test_nonauthpost(self): 
        """Невозможность публикации неавторизованным пользователем (проверка редиректа)"""
        response = self.client.post('/new/', {'text': 'text', 'group': 'Test Group'}, follow=True)
        self.assertRedirects(response, "/auth/login/?next=/new/", 302, 200)
<<<<<<< HEAD
        Set = Post.objects.count()
        self.assertEqual(Set, 1)
 
    def test_disppost(self): 
        """После публикации поста новая запись появляется на главной странице сайта (index),
        на персональной странице пользователя (profile), и на отдельной странице поста (post)""" 
        method(self)
        
    def test_updpost(self): 
        """Возможность редактирования поста авторизованным пользователем,
        проверка изменений на всех страницах""" 
        self.post = Post.objects.get(pk=1) 
        self.post.text = "Update"
        self.post.group = None
        self.post.save(update_fields=['text', 'group'])
        method(self)
=======

    def test_DispPost(self):
        """После публикации поста новая запись появляется на главной странице сайта (index), """
        """на персональной странице пользователя (profile), и на отдельной странице поста (post)"""
        urls = (
            ('index', {}),
                ('profile', {'username': self.user.username}),
                    ('post', {'username': self.user.username, 'post_id': self.post.id})
        )
        for name, kwargs in urls:
            response = self.client.get(reverse(name, kwargs=kwargs)) #Ошибка "list indices must be integers or slices, not type" не понял, как поправить
            if Paginator in response.context:
                self.assertEqual(response.context['Page'].user, self.user)
                self.assertEqual(response.context['Page'].text, self.text)
                self.assertEqual(response.context['Page'].group, self.group.id)
            else:
                self.assertEqual(response.context['post'].user, self.user)
                self.assertEqual(response.context['post'].text, self.text)
                self.assertEqual(response.context['post'].group, self.group.id)

    def test_UpdPost(self):
        """Возможность редактирования поста авторизованным пользователем"""
        """Проверка изменений на всех страницах"""
        self.post = Post.objects.get(pk=1)
        self.post.text = "Update"
        self.post.save(update_fields=['text'])
        self.test_DispPost()
>>>>>>> 3f014c9be953bb38f7ee8faa4479f346c5d6f1b5
