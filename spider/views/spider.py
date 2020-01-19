from spider.models import SpiderConfig
from django.shortcuts import render
import requests


def list(request):
    cfg = SpiderConfig.objects.all()
    return render(request, 'spider/list.html', {'cfg': cfg})



"""开启爬虫"""
def start_scrapy(request,id):
    spider = SpiderConfig.objects.get(id=id)
    spider_name = spider.name
    url = 'http://127.0.0.1:6800/schedule.json'
    if spider_name == 'jd_spider':
        project = 'cu_spiders'
    else:
        project = 'cu2_spiders'
    data = {'project': project, 'spider': spider_name}
    spider.status = 1
    spider.save()
    print(requests.post(url=url, data=data))
    return render(request, 'spider/list.html', {'cfg': SpiderConfig.objects.all()})

"""关闭爬虫"""
def stop_scrapy(request,id):
    spider = SpiderConfig.objects.get(id=id)
    spider_name = spider.name
    url = 'http://127.0.0.1:6800/cancel.json'
    if spider_name == 'jd_spider':
        project = 'cu_spiders'
    else:
        project = 'cu2_spiders'
    data = {'project': project, 'spider': spider_name}
    spider.status = 0
    spider.save()
    print(requests.post(url=url, data=data))
    return render(request, 'spider/list.html', {'cfg': SpiderConfig.objects.all()})