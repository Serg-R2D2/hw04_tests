from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from django.test import Client
from .models import Post


class TestMethods(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                        username="User", 
                        email="User@skynet.com", 
                        password="User"
                        )
        self.post = Post.objects.create(
            text=f"А теперь ты приходишь и говоришь: "
            f"Дон Корлеоне, мне нужна справедливость." 
            f"Но ты не просишь с уважением, не предлагаешь дружбу, "
            f"даже не думаешь обратиться ко мне — крёстный.", 
            author=self.user)
        
    def test_Profile(self):
        """Проверка создания персональной страницы после регистрации"""
        response = self.client.get("/User/")
        self.assertEqual(response.status_code, 200, msg='Страница не создана')
    
    def test_AuthPost(self):
        """Возможность публикации авторизованным пользователем"""
        post_url = reverse('post', args=(self.post.author, self.post.id,))
        response = self.client.get(post_url)
        self.assertEqual(response.status_code, 200, msg='Публикация не создана')

    def test_NonAuthPost(self):
        """Невозможность публикации неавторизованным пользователем (проверка редиректа)"""
        response = self.client.get("/new/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/new/", 302, 200)

    def test_DispPost(self):
        """После публикации поста новая запись появляется на главной странице сайта (index), """
        """на персональной странице пользователя (profile), и на отдельной странице поста (post)"""
        response = self.client.get("")
        self.assertContains(response, self.post.text, count=1)
        post_url1 = reverse('profile', args=(self.post.author,))
        response1 = self.client.get(post_url1)
        self.assertContains(response, self.post.text, count=1)
        post_url2 = reverse('post', args=(self.post.author, self.post.id,))
        response2 = self.client.get(post_url2)
        self.assertContains(response, self.post.text, count=1)

    def test_UpdPost(self):
        """Возможность редактирования поста авторизованным пользователем"""
        """Проверка изменений на всех страницах"""
        self.post = Post.objects.get(pk=1)
        self.post.text = "Update"
        self.post.save(update_fields=['text'])
        self.test_DispPost()

