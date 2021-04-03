import logging
FORMAT = '%(asctime)s-%(name)s-%(funcName)s:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

from django.shortcuts import render
from django.http import HttpResponse

def links(request):
    logging.debug(request)
    return HttpResponse('links')
    # return render(request, 'config/links.html', context={'name': 'links'})
