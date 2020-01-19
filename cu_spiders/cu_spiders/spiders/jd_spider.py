# -*- coding: utf-8 -*-
import scrapy
from cu_spiders.items import JDGoodsItem
import re

'''从京东商城爬取商品'''""
class JdSpiderSpider(scrapy.Spider):
    name = 'jd_spider'
    allowed_domains = ['jd.com']
    start_urls = []
    # 设置搜索内容
    search_test = ['中国移动', '中国联通', '中国电信']
    base_url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % search_test[1]
    for page in range(100):
        start_urls.append(base_url + '&page=' + str(page*2+1))

    def parse(self, response):
        goods = response.xpath('//li[@class="gl-item"]')
        goodsid = goods.xpath('@data-sku').extract()
        goodsname = goods.xpath('//div[@class="p-name p-name-type-2"]//em/text()').extract()
        goodsprice= goods.xpath('//div[@class="p-price"]//i//text()').extract()
        goodshop = goods.xpath('//div[@class="p-shop"]//a/text()').extract()
        for i in range(len(goodsid)):
            item = JDGoodsItem()
            item['goodid'] = goodsid[i]
            item['goodsname'] = goodsname[i]
            item['goodprice'] = goodsprice[i]
            item['goodshop'] = goodshop[i]
            # 设置当前爬取商品运营商 1：中国移动 2：中国联通 3：中国电信 4：未知
            item['type'] = 2
            item['goodurl'] = 'https://item.jd.com/%s.html' % goodsid[i]
            item['page'] = re.search(r'page=(\d+)', response.url).group(1)
            yield item