import os
import django
import sys
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'npcs.settings'
django.setup()

"""重复销量计算脚本"""
from spider.models import JDGoods
from django.db.models import Sum
goods = JDGoods.objects.all().order_by('goodid')
temp_num = goods[0].comment_num
temp_goodshop = goods[0].goodshop
count = 0
for i in goods[1:]:
    if temp_num == i.comment_num and temp_goodshop == i.goodshop:
        i.num_flag = 1
        i.save()
        print(i.goodid)
        count += 1
    temp_num = i.comment_num
    temp_goodshop = i.goodshop

# cm_goods = JDGoods.objects.filter(type=1, num_flag=0).values('good_type').annotate(sum=Sum('comment_num')).order_by('good_type')
# cu_goods = JDGoods.objects.filter(type=2, num_flag=0).values('good_type').annotate(sum=Sum('comment_num')).order_by('good_type')
# ct_goods = JDGoods.objects.filter(type=3, num_flag=0).values('good_type').annotate(sum=Sum('comment_num')).order_by('good_type')
# print(cm_goods)
# print(cu_goods)
# print(ct_goods)

# from spider.models import JDGoods
# ls = JDGoods.objects.raw("""SELECT * FROM spider_jdgoods where goodshop like '%移动%旗舰店%';""")
# print(ls)