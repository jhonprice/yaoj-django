from logging import getLogger

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import Problem, StaticPage, Submission
from .judge import judge


def index(request):
    index_page = get_object_or_404(StaticPage, slug='index')
    return render(request, 'z/index.html', {'content': index_page.content})


def faq(request):
    faq_page = get_object_or_404(StaticPage, slug='faq')
    return render(request, 'z/faq.html', {'content': faq_page.content})


def problem_list(request):
    problems = Problem.objects.order_by('id')
    return render(request, 'z/problem_list.html', {'problems': problems})


def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'z/problem_detail.html', {'problem': problem})


@login_required
def problem_submit(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.method == 'GET':
        return render(request, 'z/problem_submit.html', {'problem': problem})
    else:
        s = Submission(author=request.user.member, problem=problem,
                       source_code=request.POST['src'])
        s.save()
        judge.delay(s.id)
        return redirect(reverse('z:problem_status', args=(problem_id, )))


def problem_status(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'z/problem_status.html', {'problem': problem})
