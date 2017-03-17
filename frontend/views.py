import json
import time

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page

from backend.meituan_crawer import MeituanCrawler


# Create your views here.

def index(request):
    template = loader.get_template('frontend/index.html')
    return HttpResponse(template.render())


# @cache_page(60 * 15)
def search(request):
    crawler = MeituanCrawler()

    if request.GET.get('ids'):
        # note: 美团外卖的id会经常变化，使用该接口时请确定是最新获取的
        shop_url = 'http://waimai.meituan.com/restaurant/{id}'
        ids = request.GET.get('ids').split(',')

        urls = list(map(lambda x: shop_url.format(id=x.strip()), ids))


        crawler.parse_urls(urls)
        wb,filename = crawler.wb, 'results_{time}.xls'.format(time=time.strftime('%Y-%m-%d_%H-%M-%S'))

        # return HttpResponse(str(urls))
        pass
    else:
        city = request.GET.get('city')
        name = request.GET.get('name')

        wb, filename = crawler.run(city, name)
        pass

    from pypinyin import lazy_pinyin
    filename = ''.join(lazy_pinyin(filename))

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename={file_name}'.format(file_name=filename)
    wb.save(response)

    return response
    pass
