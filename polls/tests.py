import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Polls are available")
        self.assertQuerysetEqual(response.context['question_list'],[])
    
    def test_past_question(self):
        question = create_question(question_text='past', days=-30)
        question.choice_set.create(choice_text='hoge')
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "past")
    
    def test_future_question(self):
        question=create_question('future', days=30)
        question.choice_set.create(choice_text='hoge')
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Polls are available")
    
    def test_question_without_choice(self):
        q_with_choice = create_question('I have a choice', days=-1)
        q_without_choice = create_question('I dont have a choice', days=-1)
        q_with_choice.choice_set.create(choice_text='I am choice')
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,'I have a choice')
        self.assertNotContains(response,'I dont have a choice')

class DetailViewTests(TestCase):

    def test_past_question(self):
        question=create_question('past', days=-30)
        question.choice_set.create(choice_text='hoge')
        response=self.client.get(reverse('polls:detail',args=[question.id]))
        self.assertContains(response,question.question_text)

class QuestionModelTests(TestCase):
    
    def test_future_question_return_false_for_wasPublishedRecentry_method(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_too_old_question_return_false_for_wasPublishedRecentry_method(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(),False)
    
    def test_recent_question_return_true_for_wasPublishedRecentry_method(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        question = Question(pub_date = time)
        self.assertIs(question.was_published_recently(),True)
# Create your tests here.
