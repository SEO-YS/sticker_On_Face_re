#from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from common.ai_process import put_sticker
from common.forms import UserForm
from datos.models import Question, Question2, Question3, Question4,Images2
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def cctv(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')

    # question_list = Question.objects.annotate()

    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 4)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)
    context = {'question_list': page_obj, 'max_index': max_index, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'common/cctv.html', context)
def conclusion(request):
    return render(request, 'common/conclusion.html')

def population(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')

    # question_list = Question.objects.annotate()

    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 4)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)
    context = {'question_list': page_obj, 'max_index': max_index, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'common/population.html', context)

def seoul_pop(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')

    # question_list = Question.objects.annotate()

    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')


    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 4)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)
    context = {'question_list': page_obj, 'max_index': max_index, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'common/seoul_pop.html', context)



def imageUpload(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        print(image_file)

        # 모델 인스턴스 생성 및 필드에 값 할당
        your_model_instance = Images2()
        your_model_instance.image = image_file
        your_model_instance.author = request.user
        print(your_model_instance.image)

        # 아래는 AI 작업 1줄
        # your_model_instance = put_sticker(your_model_instance)

        your_model_instance.save()
        print(your_model_instance.image)

        print(your_model_instance.image)
        print(your_model_instance.image.url)
        response_data = {
            'filepath': your_model_instance.image.url,
            'additional_info': 'Additional information you want to pass',
        }
        print(your_model_instance.image.path)
        return JsonResponse(response_data)
    return JsonResponse({'success': 'True'})