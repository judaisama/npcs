from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from spider.models import JDGoods


def list(request):
    good_list = JDGoods.objects.all()
    if request.method == "GET":
        goodname = request.GET.get('goodname', None)
        if goodname:
            good_list = good_list.filter(goodsname__contains=goodname)
    paginator = Paginator(good_list, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'analyse/shop_list.html', {'contacts': contacts})


def detail(request,goodid):
    good = JDGoods.objects.get(goodid=goodid)
    return render(request, 'analyse/good_detail.html', {'good': good})