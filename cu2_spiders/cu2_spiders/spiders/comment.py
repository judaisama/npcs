# -*- coding: utf-8 -*-
import scrapy
from spider.models import JDGoodsComment, JDGoods
import json

'''获得商品评论'''
class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['jd.com']
    goods = JDGoods.objects.filter(flag=0)
    start_urls = []
    for i in goods:
        start_urls.append('https://item.jd.com/%s.html' % i.goodid)

    def parse(self, response):
        goodid = response.url[20:][:-5]
        good = JDGoods.objects.get(goodid=goodid)
        if good.cv != -1 and good.comment_num and good.flag == 0:
            fetch = 'fetchJSON_comment98vv%s' % good.cv
            page = self.get_page(good.comment_num)
            for k in range(0, int(page)):
                url = 'https://sclub.jd.com/comment/productPageComments.action?' \
                      'callback=%s&productId=%s&score=0&' \
                      'sortType=5&page=%s&pageSize=10' % (fetch, goodid, k)
                yield scrapy.Request(url, meta={'fetch': fetch, 'goodid': goodid}, callback=self.parse_getCommentnum)
            good.flag = 1
            good.save()
        else:
            print('goodid'+goodid+':pass')

    def parse_getCommentnum(self, response):
        try:
            data, goodid = self.get_data(response)
            for comment in data['comments']:
                comment = JDGoodsComment(good_id_id=goodid, user_info=comment['nickname'], star=comment['score'],
                           content=comment['content'], date=comment['referenceTime'])
                comment.save()
        except Exception as e:
            print(e)
            print('error page')

    def get_page(self, comment_num):
        if int(comment_num) % 10 == 0:
            page = int(comment_num) / 10
        else:
            page = int(comment_num) / 10 + 1
        return page

    def get_data(self, response):
        temp1 = response.body.decode('gbk')
        dic = response.meta
        data = temp1.replace(dic['fetch'], '')
        data = data.replace('(', '')
        data = data.replace(')', '')
        data = data.replace(';', '')
        data = json.loads(data)
        return data, dic['goodid']
