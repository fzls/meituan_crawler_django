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
    city = request.GET.get('city')
    name = request.GET.get('name')
    ids = request.GET.get('ids')

    crawler = MeituanCrawler()
    wb, filename = crawler.run(city, name, ids)

    from pypinyin import lazy_pinyin
    filename = ''.join(lazy_pinyin(filename))

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename={file_name}'.format(file_name=filename)
    wb.save(response)

    return response
    pass
