from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from spider.models import JDGoodsComment


def list(request):
    good_list = JDGoodsComment.objects.all()
    paginator = Paginator(good_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'analyse/comment_list.html', {'contacts': contacts})


def one_good(request, goodid):
    com_list = JDGoodsComment.objects.filter(good_id_id=goodid)
    paginator = Paginator(com_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'analyse/comment_list.html', {'contacts': contacts})