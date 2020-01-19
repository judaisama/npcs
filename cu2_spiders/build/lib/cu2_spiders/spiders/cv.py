# -*- coding: utf-8 -*-
import scrapy
from spider.models import JDGoods
import re
import json

'''获得commentVersion和商品总评价数'''
class JdSpiderSpider(scrapy.Spider):
    name = 'cv'
    allowed_domains = ['jd.com']
    goods = JDGoods.objects.all()
    start_urls = []
    for i in goods:
        start_urls.append('https://item.jd.com/%s.html#comments-list' % i.goodid)

    def parse(self, response):
        goodid = re.search(r'(\d+)', str(response.url)).group(1)
        print(goodid)
        cv = re.search(r'commentVersion:\D*(\d+)\D*,', str(response.body))
        dic = {'goodid': goodid}
        if cv and cv.group(1):
            dic['cv'] = cv.group(1)
            print(dic['cv'])
        else:
            dic['cv'] = -1

        url = "http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=%s" % goodid
        yield scrapy.Request(url, meta=dic, callback=self.parse_getCommentnum)


    def parse_getCommentnum(self, response):
        dic = response.meta
        temp = json.loads(response.body)
        try:
            good = JDGoods.objects.get(goodid=dic['goodid'])
            good.cv = dic['cv']
            good.comment_num = temp['CommentsCount'][0]['CommentCount']
            good.score1_num = temp['CommentsCount'][0]['Score1Count']
            good.score2_num = temp['CommentsCount'][0]['Score2Count']
            good.score3_num = temp['CommentsCount'][0]['Score3Count']
            good.score4_num = temp['CommentsCount'][0]['Score4Count']
            good.score5_num = temp['CommentsCount'][0]['Score5Count']
            good.comment_default_num = temp['CommentsCount'][0]['DefaultGoodCount']
            good.goodrate = temp['CommentsCount'][0]['GoodRate']
            good.save()
            print(dic['goodid'] + '写入成功')
        except Exception as e:
            print(e)
            print(dic['goodid']+'写入失败')

