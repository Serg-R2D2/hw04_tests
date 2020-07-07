from django.contrib.auth.models import User 
from django.core.paginator import Paginator 
from django.shortcuts import reverse 
from django.test import TestCase 
from django.test import Client 
from .models import Post, Group 


class TestMethods(TestCase):
    def check_post_data(self, urls, text, group, author):
        for name, kwargs in urls:
            response = self.client.get(reverse(name, kwargs=kwargs))
            paginator = response.context.get('paginator')
        if paginator is not None:
            post = response.context['page'][0]
        else:
            post = response.context['post']
        self.assertEqual(post.text, text)
        self.assertEqual(post.author, author)
        self.assertEqual(post.group, group)

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
        
    def test_profile(self): 
        """Проверка создания персональной страницы после регистрации"""
        response = self.client.get("/User/") 
        self.assertEqual(
            response.status_code, 
            200, 
            msg='Страница не создана'
            )

    def test_authpost(self): 
        """Возможность публикации авторизованным пользователем"""
        entrance = self.client.force_login(self.user)
        response = self.client.post(
            reverse("new_post"), 
            {
                'text': 'text', 
                'group': self.group.id
            },
            follow=True
            )
        self.assertEqual(
            response.status_code,
            200, 
            msg='Публикация невозможна'
            )
        Set = Post.objects.count()
        self.assertEqual(Set, 1)
        LP = Post.objects.first()
        self.assertEqual(LP.text, 'text')
        self.assertEqual(LP.author, self.user)
        self.assertEqual(LP.group, self.group)

    def test_nonauthpost(self):
        """Невозможность публикации неавторизованным пользователем (проверка редиректа)"""
        response = self.client.post(
            reverse("new_post"),
            {
                'text': 'text',
                'group': self.group.id
            }, 
            follow=True
            )
        self.assertRedirects(response, "/auth/login/?next=/new/", 302, 200)
        Set = Post.objects.count()
        self.assertEqual(Set, 0)
 
    def test_disppost(self): 
        """После публикации поста новая запись появляется на главной странице сайта (index),
        на персональной странице пользователя (profile), и на отдельной странице поста (post)"""
        self.post = Post.objects.create(
                        text="А теперь ты приходишь и говоришь: "+
                        "Дон Корлеоне, мне нужна справедливость."+
                        "Но ты не просишь с уважением, не предлагаешь дружбу, "+
                        "даже не думаешь обратиться ко мне — крёстный.",  
                        author=self.user, 
                        group = self.group
                        ) 
        urls = ( 
            ('index', {}), 
            ('profile', {'username': self.user.username}), 
            ('post', {'username': self.user.username, 'post_id': self.post.id}) 
            )
        text = self.post.text
        group = self.group
        author = self.post.author
        self.check_post_data(urls, text, group, author)

    def test_updpost(self): 
        """Возможность редактирования поста авторизованным пользователем,
        проверка изменений на всех страницах"""
        self.post = Post.objects.create(
                        text="А теперь ты приходишь и говоришь: "+
                        "Дон Корлеоне, мне нужна справедливость."+
                        "Но ты не просишь с уважением, не предлагаешь дружбу, "+
                        "даже не думаешь обратиться ко мне — крёстный.",  
                        author=self.user, 
                        group=self.group
                        ) 
        entrance = self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                "post_edit", 
                kwargs={
                    'username': self.user.username, 
                    'post_id': self.post.id}
                    ), 
                {
                'text': 'Update', 
                'group': ''
                }, 
                follow=True)
        urls = ( 
            ('index', {}), 
            ('profile', {'username': self.user.username}), 
            ('post', {'username': self.user.username, 'post_id': self.post.id}) 
            )
        self.post = Post.objects.last()
        text = self.post.text
        group = self.post.group 
        author = self.post.author
        self.check_post_data(urls, text, group, author)

    def test_404(self):
        response = self.client.get("/page_do_not_exist/", follow=True)
        self.assertEqual(response.status_code, 404)
