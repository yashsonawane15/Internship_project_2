from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from mongoengine import *
from fetcher.views import status

def testView(request):
	return JsonResponse(status.objects.to_json())