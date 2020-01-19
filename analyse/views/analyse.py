from django.shortcuts import render
from spider.models import JDGoods, JDGoodsComment
from django.db.models import Sum
import json


def home(request):
    return render(request, 'analyse/home.html')


def index(request):
    dicts = {}
    dicts['data'] = json.dumps(get_operator_data(0))
    dicts['total'] = get_total(0)
    dicts['top5'] = get_top5_good(0)
    return render(request, 'analyse/index.html', dicts)

def index2(request):
    dicts = {}
    dicts['data'] = json.dumps(get_operator_data(1))
    dicts['total'] = get_total(1)
    dicts['top5'] = get_top5_good(1)
    return render(request, 'analyse/index2.html', dicts)

"""三大运营商top5数据总数生成计算"""
def get_top5_good(flagship):
    if flagship == 1:  # 官方旗舰店
        goods_cm = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =1 and is_flagship =1 GROUP BY comment_default_num ORDER BY comment_num DESC")
        goods_cu = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =2 and is_flagship =1 GROUP BY comment_default_num ORDER BY comment_num DESC")
        goods_ct = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =3 and is_flagship =1 GROUP BY comment_default_num ORDER BY comment_num DESC")
        goodrate_cm = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =1 and comment_num > 10 and is_flagship =1 GROUP BY goodrate ORDER BY goodrate DESC")
        goodrate_cu = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =2 and comment_num > 10 and is_flagship =1 GROUP BY goodrate ORDER BY goodrate DESC")
        goodrate_ct = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =3 and comment_num > 10 and is_flagship =1 GROUP BY goodrate ORDER BY goodrate DESC")
    else:
        goods_cm = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =1 GROUP BY comment_default_num ORDER BY comment_num DESC")
        goods_cu = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =2 GROUP BY comment_default_num ORDER BY comment_num DESC")
        goods_ct = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =3 GROUP BY comment_default_num ORDER BY comment_num DESC")
        goodrate_cm = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =1 and comment_num > 10 GROUP BY goodrate ORDER BY goodrate DESC")
        goodrate_cu = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =2 and comment_num > 10 GROUP BY goodrate ORDER BY goodrate DESC")
        goodrate_ct = JDGoods.objects.raw("SELECT * FROM `spider_jdgoods` where num_flag=0 and type =3 and comment_num > 10 GROUP BY goodrate ORDER BY goodrate DESC")
    return [[goods_cm[:5], goods_cu[:5], goods_ct[:5]], [goodrate_cm[:5], goodrate_cu[:5], goodrate_ct[:5]]]


"""三大运营商数据总数生成计算"""
def get_total(flagship):
    if flagship == 1:  # 官方旗舰店
        goods = JDGoods.objects.filter(is_flagship=1)
        comment = JDGoodsComment.objects.filter(good_id__is_flagship=1)
        num = JDGoods.objects.filter(num_flag=0, is_flagship=1).aggregate(sum=Sum('comment_num'))
        shop_num = JDGoods.objects.filter(num_flag=0, is_flagship=1).values('goodshop').annotate(sum=Sum('goodshop'))
    else:
        goods = JDGoods.objects.all()
        comment = JDGoodsComment.objects.all()
        num = JDGoods.objects.filter(num_flag=0).aggregate(sum=Sum('comment_num'))
        shop_num = JDGoods.objects.filter(num_flag=0).values('goodshop').annotate(sum=Sum('goodshop'))
    return [goods.count(), num['sum'], shop_num.count(), comment.count()]


"""三大运营商对比数据生成计算"""
def get_operator_data(flagship):
    dicts = {}
    if flagship == 1:  # 官方旗舰店
        #三大运营商销量数据
        goods = JDGoods.objects.filter(num_flag=0, is_flagship=1).values('type').annotate(sum=Sum('comment_num')).order_by('type')
        # 三大运营商各类别销量数据
        cm_goods = JDGoods.objects.filter(type=1, num_flag=0, is_flagship=1).values('good_type').annotate(sum=Sum('comment_num')).order_by('good_type')
        cu_goods = JDGoods.objects.filter(type=2, num_flag=0, is_flagship=1).values('good_type').annotate(sum=Sum('comment_num')).order_by('good_type')
        ct_goods = JDGoods.objects.filter(type=3, num_flag=0, is_flagship=1).values('good_type').annotate(sum=Sum('comment_num')).order_by('good_type')
    else:
        #三大运营商销量数据
        goods = JDGoods.objects.filter(num_flag=0).values('type').annotate(sum=Sum('comment_num')).order_by('type')
        # 三大运营商各类别销量数据
        cm_goods = JDGoods.objects.filter(type=1, num_flag=0).values('good_type').annotate(sum=Sum('comment_num')).order_by('good_type')
        cu_goods = JDGoods.objects.filter(type=2, num_flag=0).values('good_type').annotate(sum=Sum('comment_num')).order_by('good_type')
        ct_goods = JDGoods.objects.filter(type=3, num_flag=0).values('good_type').annotate(sum=Sum('comment_num')).order_by('good_type')

    com_dic = get_sum(goods, 'type', 3, 'total_goods')
    cm_goods_dic = get_sum(cm_goods, 'good_type', 5, 'cm_goods')
    cu_goods_dic = get_sum(cu_goods, 'good_type', 5, 'cu_goods')
    ct_goods_dic = get_sum(ct_goods, 'good_type', 5, 'ct_goods')
    dicts['com_dic'] = com_dic
    dicts['cm_goods_dic'] = cm_goods_dic
    dicts['cu_goods_dic'] = cu_goods_dic
    dicts['ct_goods_dic'] = ct_goods_dic

    return dicts

def get_sum(goods, goodstype, num, keyname):
    dic = {}
    for good in goods:
        for i in range(1, num+1):
            if good[goodstype] == i:
                dic[keyname+'_'+str(i)] = int(good['sum'])
    return dic