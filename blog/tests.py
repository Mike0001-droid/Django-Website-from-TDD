from audioop import reverse
from django.urls import resolve
from django.test import TestCase
from blog.views import home_page, article_page
from blog.models import Article
from django.http import HttpRequest
from django.urls import reverse
from datetime import datetime
import pytz


class ArticlePageTest(TestCase):

    def test_article_page_displays_correct_article(self):
        Article.objects.create(
            title='title 1',
            summary='summary 1',
            full_text='full_text 1',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug = 'ooo-lya-lya'
        )

        request = HttpRequest()
        response = article_page(request, 'ooo-lya-lya')
        html = response.content.decode('utf8')

        self.assertIn('title 1', html)
        self.assertIn('full_text 1', html)
        self.assertNotIn('summary 1', html)
        

class HomePageTest(TestCase):

    def test_home_page_displays_articles(self):
        Article.objects.create(
            title='title 1',
            summary='summary 1',
            full_text='full_text 1',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug = 'slug-1'
        )
        Article.objects.create(
            title='title 2',
            summary='summary 2',
            full_text='full_text 2',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug = 'slug-2'
        )

        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')

        self.assertIn('title 1', html)
        self.assertIn('/blog/slug-1',html)
        self.assertIn('summary 1', html)
        self.assertNotIn('full_text 1', html)

        self.assertIn('title 2', html)
        self.assertIn('/blog/slug-2', html)
        self.assertIn('summary 2', html)
        self.assertNotIn('full_text 2', html)
        

    def test_home_page_returns_correct_html(self):
        url = reverse('home_page')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'home_page.html')

class ArticleModelTest(TestCase):
    def test_article_model_self_and_retrieve(self):
        #Создай статью 1
        #Сохрани статью 1 в базе
        article1 = Article(
            title='article 1', 
            full_text='full_text 1',
            summary='summary 1',
            categery='category 1',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug= 'slug-1'
        )
        article1.save()

        #Создай статью 2
        #Сохрани статью 2 в базе
        article2 = Article(
            title='article 2', 
            full_text='full_text 2',
            summary='summary 2',
            categery='category 2',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug= 'slug-2'
        )
        article2.save()

        #Загрузи из базы все статьи
        all_articles = Article.objects.all()

        #Проверь: статьи должно быть две
        self.assertEqual(len(all_articles),2)


        #Проверь: первая, загруженная из базы == статья 1
        self.assertEqual(
            all_articles[0].title,
            article1.title
        )

        self.assertEqual(
            all_articles[0].slug,
            article1.slug
        )

        self.assertEqual(
            all_articles[1].title,
            article2.title
        )

        self.assertEqual(
            all_articles[1].slug,
            article2.slug
        )