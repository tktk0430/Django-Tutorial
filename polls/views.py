from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
    model = Question

class DetailView(generic.DetailView):
    model = Question

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

'''
汎用ビューを使わない書き方
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    urlName = reverse('polls:index')
    context = {
        'latest_question_list' : latest_question_list,
        'urlName' : urlName
    }
    return render(request,'polls/index.html', context)

def detail(request, question_id):
    urlName = reverse('polls:detail', args=[question_id])
    # try:
    #     question = Question.objects.get(pk = question_id)
    # except:
    #     raise Http404("this question does not exist.")
    question = get_object_or_404(Question, pk=question_id)
    context = {"question":question, "urlName":urlName}
    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    response = "You're looking at the results of question %s."
    return render(request, 'polls/results.html', {"question":question, "response":response})
'''

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/question_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        import pdb; pdb.set_trace()
        return HttpResponseRedirect(reverse('polls:results', args=[question.id]))

