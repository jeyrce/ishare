# coding=utf-8
from django.shortcuts import render
from django.views.generic import View


# Create your views here.
class BizIndex(View):

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request, 'biz/index.html', ctx)
