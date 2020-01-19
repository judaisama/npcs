from django.db import models

'''京东商品表'''
class JDGoods(models.Model):
    type_choices = ((1, '中国移动'), (2, '中国联通'), (3, '中国电信'), (4, '未知'))
    good_type_choices = ((1, '电话卡'), (2, '宽带'), (3, '手机'), (4, '路由器'), (5, '其它'))
    flag_choices = ((0, '未爬取'), (1, '已爬取'))
    flagship_choices = ((0, '否'), (1, '是'))
    num_flag_choices = ((0, '否'), (1, '是'))
    goodid = models.CharField(verbose_name="商品编号", max_length=128, primary_key=True)
    goodsname = models.CharField(verbose_name="商品名", max_length=256)
    goodshop = models.CharField(verbose_name="商铺名", max_length=128)
    goodprice = models.CharField(verbose_name="价格", max_length=128)
    comment_num = models.IntegerField(verbose_name="总评价数")
    goodurl = models.CharField(verbose_name="商品链接", max_length=256)
    cv = models.CharField(verbose_name="评论编号", max_length=128)
    type = models.IntegerField(verbose_name="类别", choices=type_choices, default=4)
    good_type = models.IntegerField(verbose_name="商品类别", choices=good_type_choices, default=5)
    page = models.IntegerField(verbose_name="页数")
    flag = models.IntegerField(verbose_name="该商品评论是否爬取", choices=flag_choices, default=0)
    num_flag = models.IntegerField(verbose_name="该商品评论数量是否重复", choices=num_flag_choices, default=0)
    score1_num = models.IntegerField(verbose_name="1星评价数")
    score2_num = models.IntegerField(verbose_name="2星评价数")
    score3_num = models.IntegerField(verbose_name="3星评价数")
    score4_num = models.IntegerField(verbose_name="4星评价数")
    score5_num = models.IntegerField(verbose_name="5星评价数")
    comment_default_num = models.IntegerField(verbose_name="默认好评数")
    goodrate = models.CharField(verbose_name="好评率", max_length=128)
    is_flagship = models.IntegerField(verbose_name="是否为官方旗舰店", choices=flagship_choices, default=0)
    c_time = models.DateTimeField(verbose_name="爬取时间", auto_now_add=True)



'''京东商品评论表'''
class JDGoodsComment(models.Model):
    sentiment_choices = ((1, '满意'), (2, '一般'), (3, '不满意'), (4, '未知'))
    good_id = models.ForeignKey(JDGoods, related_name="comment", on_delete=models.PROTECT)
    user_info = models.CharField(verbose_name="评论用户名", max_length=256)
    star = models.CharField(verbose_name="评分", max_length=10)
    content = models.CharField(verbose_name="评论内容", max_length=256)
    date = models.CharField(verbose_name="评论时间", max_length=20)
    c_time = models.DateTimeField(verbose_name="爬取时间", auto_now_add=True)
    sentiment = models.IntegerField(verbose_name="用户情感", choices=sentiment_choices, default=4)

    def deal_content(self):
        return self.content.strip()

    def deal_date(self):
        return self.date[:10]

class SpiderConfig(models.Model):
    choices = ((1, '已开启'), (0, '已关闭'))
    name = models.CharField(verbose_name="爬虫名", max_length=256)
    description = models.CharField(verbose_name="描述", max_length=256)
    status = models.IntegerField(verbose_name="用户情感", choices=choices, default=0)

    def start_spider(self):
        self.status = 1
        self.save()

    def stop_spider(self):
        self.status = 0
        self.save()
