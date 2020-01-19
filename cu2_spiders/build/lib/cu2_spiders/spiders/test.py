# -*- coding: utf-8 -*-
import scrapy
from spider.models import JDGoods,JDGoodsComment
import json
import re

'''刷新京东商品描述'''
class JdSpiderSpider(scrapy.Spider):
    name = 'refreshname'
    allowed_domains = ['jd.com']
    #goods = JDGoods.objects.all()
    goods = JDGoods.objects.filter(goodsname='')
    start_urls = []
    for i in goods:
        start_urls.append(i.goodurl)
        #start_urls.append('https://cartv.jd.com/item/%s.html' % i.goodid)

    def parse(self, response):
        try:
            goodid = re.search(r'(\d+)', str(response.url)).group(1)
            goodsname = response.xpath('//div[@class="sku-name"]/text()').extract()
            #goodsname = response.xpath('//p[@class="fi-r-title"]/text()').get()
            good = JDGoods.objects.get(goodid=goodid)
            print(str(goodsname[1]).strip())
            #good.goodsname = str(goodsname).strip()
            good.goodsname = str(goodsname[1]).strip()
            good.save()
            print('更新', goodid)
        except Exception as e:
            print(e)


# '''手动填补京东商品评论'''
# class JdSpiderSpider(scrapy.Spider):
#     name = 'refreshcomment'
#     allowed_domains = ['jd.com']
#     #goods = JDGoods.objects.all()
#     #goods = JDGoods.objects.filter(goodsname='None')
#     goods = [57062912939,57062912940,57062912942,57062912944,57062912946,57146459744,57146459745,57146459746,48345834318,48345834319,48345834320,48345834321,
#              48346653884,48346653885,48347511449,48347511450,48349709791,48349709792,48357310833,48357310834,47820783853,47820783854,47820783855,47820783856,
#              47820783857]
#     start_urls = ['https://item.jd.com/57062912938.html']
#     for i in goods:
#         #start_urls.append(i.goodurl)
#         start_urls.append('https://item.jd.com/%s.html' % i)
#
#     def parse(self, response):
#         goodid = response.url[20:][:-5]
#         good = JDGoods.objects.get(goodid=goodid)
#         if good.cv != -1 and good.comment_num:
#             fetch = 'fetchJSON_comment98vv%s' % good.cv
#             page = self.get_page(good.comment_num)
#             for k in range(0, int(page)):
#                 url = 'https://sclub.jd.com/comment/productPageComments.action?' \
#                       'callback=%s&productId=%s&score=0&' \
#                       'sortType=5&page=%s&pageSize=10' % (fetch, goodid, k)
#                 yield scrapy.Request(url, meta={'fetch': fetch, 'goodid': goodid}, callback=self.parse_getCommentnum)
#             good.flag = 1
#             good.save()
#         else:
#             print('goodid' + goodid + ':pass')
#
#     def parse_getCommentnum(self, response):
#         try:
#             data, goodid = self.get_data(response)
#             for comment in data['comments']:
#                 comment = JDGoodsComment(good_id_id=goodid, user_info=comment['nickname'], star=comment['score'],
#                                          content=comment['content'], date=comment['referenceTime'])
#                 comment.save()
#         except Exception as e:
#             print(e)
#             print('error page')
#
#     def get_page(self, comment_num):
#         if int(comment_num) % 10 == 0:
#             page = int(comment_num) / 10
#         else:
#             page = int(comment_num) / 10 + 1
#         return page
#
#     def get_data(self, response):
#         temp1 = response.body.decode('gbk')
#         dic = response.meta
#         data = temp1.replace(dic['fetch'], '')
#         data = data.replace('(', '')
#         data = data.replace(')', '')
#         data = data.replace(';', '')
#         data = json.loads(data)
#         return data, dic['goodid']

# '''获得商品各星级评价'''
# class JdSpiderSpider(scrapy.Spider):
#     name = 'score'
#     allowed_domains = ['jd.com']
#     start_urls = []
#     goods = JDGoods.objects.all()
#     for i in goods:
#         start_urls.append('http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=%s' % i.goodid)
#
#     def parse(self, response):
#         temp = json.loads(response.body)
#         goodid = re.search(r'(\d+)', str(response.url)).group(1)
#         try:
#             good = JDGoods.objects.get(goodid=goodid)
#             good.comment_num = temp['CommentsCount'][0]['CommentCount']
#             good.score1_num = temp['CommentsCount'][0]['Score1Count']
#             good.score2_num = temp['CommentsCount'][0]['Score2Count']
#             good.score3_num = temp['CommentsCount'][0]['Score3Count']
#             good.score4_num = temp['CommentsCount'][0]['Score4Count']
#             good.score5_num = temp['CommentsCount'][0]['Score5Count']
#             good.comment_default_num = temp['CommentsCount'][0]['DefaultGoodCount']
#             good.goodrate = temp['CommentsCount'][0]['GoodRate']
#             good.save()
#             print(goodid + '写入成功')
#         except Exception as e:
#             print(e)
#             print(goodid + '写入失败')