from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.http import Http404
from django.views import generic
from django.utils import timezone


def index(request):
    last_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in last_question_list])
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': last_question_list
    }
    # return HttpResponse("and you are at the index!" + output)
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


def detail(request, question_id):
    # try:
    #     q = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('question does not exist')
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': q})

    # return HttpResponse("you are looking at the question %s" % question_id)


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    # response = "you are looking at result of question %s "
    # return HttpResponse(response % question_id)


class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Question


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("you are voting on question %s" % question_id)

