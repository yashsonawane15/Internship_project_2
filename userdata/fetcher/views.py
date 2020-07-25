from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.middleware import csrf
from mongoengine import *
from datetime import *
from .forms import *
import json

# Create your views here.

def index(request):
	return render(request, 'index.html')

def CategoryInsert(request):
	if request.method == 'POST':
		formdata = CategoryForm(request.POST)
		data = category()
		if formdata.is_valid():
			#print('\n\n\n {}'.format(formdata.cleaned_data))
			data.isActive = formdata.cleaned_data['isActive']
			data.catname = formdata.cleaned_data['cname']
		if data.save():
			return HttpResponseRedirect('/index')

	elif request.method == "GET":
		form = CategoryForm()
		context = {
			'form' : form,
			'formtype' : ' ',
		}
		return render(request, 'input.html', context)

def StatusInsert(request):	
	if request.method == 'POST':
		formdata = StatusForm(request.POST)
		data = status()
		if formdata.is_valid():
			data.isActive = formdata.cleaned_data['isActive']
			data.name = formdata.cleaned_data['name']
			if data.save():
				return HttpResponseRedirect('/index/success')
			else:
				return HttpResponseRedirect('/index/error')

	elif request.method == "GET":
		form = StatusForm()
		context = {
			'form' : form,
			'formtype':	' ',	
		}
		return render(request, 'input.html', context)

def UserInsert(request):
	if request.method == 'POST':
		formdata = UserForm(request.POST)
		data = user()
		if formdata.is_valid():
			data.username = formdata.cleaned_data['username']
			data.fname = formdata.cleaned_data['fname']
			data.lname = formdata.cleaned_data['lname']
			data.isActive = formdata.cleaned_data['isActive']
		if data.save():
			return HttpResponseRedirect('/index/success')
		else:
			return HttpResponseRedirect('/index/error')

	elif request.method == "GET":
		form = UserForm()
		context = {
			'form' : form,
			'formtype' : ' ',
		}
		return render(request, 'input.html', context)

def todoInsert(request):
	if request.method == 'POST':
		formdata = todoForm(request.POST)
		data = todo()
		if formdata.is_valid():
			data.description = formdata.cleaned_data['description']
			data.details = formdata.cleaned_data['details']
			#change date object to datetime
			d = formdata.cleaned_data['target_date']
			data.target_date = datetime.combine(d, datetime.min.time())
			#handle references
			data.status = status.objects(name=formdata.cleaned_data['status'])[0]
			data.category = category.objects(catname=formdata.cleaned_data['category'])[0]
			data.assigned_to = user.objects(username=formdata.cleaned_data['assigned_to'])[0]
			if data.save():
				return HttpResponseRedirect('/index/success')

			else:
				return HttpResponseRedirect('/index/error')
				
		else:
				return HttpResponseRedirect('/index/error')

	elif request.method == 'GET':
			form = todoForm()
			context = {
				'formtype' : 'todo',
				'form' : form,
			}
			return render(request, 'input-todo.html', context)

def SuccessView(request):
	if request.method == 'GET':
		return render(request, 'success.html')

def ErrorView(request):
	if request.method == 'GET':
		return render(request, 'error.html')

#view to respond to ajax calls
def listFetcher(request):
	user_list = []
	status_list = []
	category_list = []

	for u in user.objects:
		user_list.append(u.username)

	for s in status.objects:
		status_list.append(s.name)

	for c in category.objects:
		category_list.append(c.catname)
	response_dict = {
		'user_list': user_list,
		'status_list': status_list,
		'category_list': category_list,
	}
	return JsonResponse(response_dict) 

#list of fields of all collections to pass as context
fields_list = {
	'user' : ['ID', 'Username', 'First Name', 'Last Name', 'Active?', 'Created On'],
	'status' : ['ID', 'Name', 'Active?', 'Created On'],
	'category' : ['ID', 'Name', 'Active?', 'Created On'],
	'todo' : ['ID', 'Description', 'Details', 'Created on', 'Target Date', 'Status', 'Category', 'Assigned to'],
}

def displayView(request, collection):
	if collection == 'user':
		coll = user.objects
	elif collection == 'status':
		coll = status.objects
	elif collection ==  'category':
		coll = category.objects
	elif collection == 'todo':
		coll = todo.objects

	context = {
		'fields' : fields_list[collection],
		'collection' : coll,
		'to_display' : collection,
	}
	
	return render(request, 'display.html', context)

def DeleteDocument(request):
	d = {}
	d['collection'] = request.GET.get('collection')
	d['id'] = request.GET.get('id')
	if d['collection'] == 'user':
		if todo.objects(assigned_to=d['id']):
			return JsonResponse({'success':False}, status=400)
		else:
			user.objects(id=d['id']).delete()

	elif d['collection'] == 'status':
		if todo.objects(status=d['id']):
			return JsonResponse({'success':False}, status=400)
		else:
			status.objects(id=d['id']).delete()

	elif d['collection'] == 'category':
		if todo.objects(category=d['id']):
			return JsonResponse({'success':False}, status=400)
		else:
			category.objects(id=d['id']).delete()

	elif d['collection'] == 'todo':
		todo.objects(id=d['id']).delete()

	return JsonResponse({'success':True}, status=200)

def ModifyDocument(request):
	d = {}
	d = request.GET.dict()
	colln = d['collection']
	mid = d['id']
	#d = json.loads(d['modified'])

	if colln == 'user':
		u = user(id=mid)
		u.username = d['username']
		u.fname = d['fname']
		u.lname = d['lname']
		if d['isActive'] == 'False' or d['isActive'] == 'false':
			u.isActive = False
		else:
			u.isActive = True
		u.createdOn = d['createdOn']
		if not u.save():
			return JsonResponse({'success':False}, status=400)
	elif colln == 'status':
		s = status(id=mid)
		s.name = d['name']
		if d['isActive'] == 'False' or d['isActive'] == 'false':
			s.isActive = False
		else:
			s.isActive = True
		s.createdOn = d['createdOn'] 
		if not s.save():
			return JsonResponse({'success':False}, status=400)

	elif colln == 'category':
		c = category(id=mid)
		c.catname = d['catname']
		if d['isActive'] == 'False' or d['isActive'] == 'false':
			c.isActive = False
		else:
			c.isActive = True
		c.createdOn = d['createdOn'] 
		if not c.save():
			return JsonResponse({'success':False}, status=400)

	elif colln == 'todo':
		t = todo(id=mid)
		t.description = d['description']
		t.details = d['details']
		t.createdOn = d['createdOn']
		t.target_date = d['target_date']
		t.status = status.objects(name=d['status'])[0].id
		t.category = category.objects(catname=d['category'])[0].id
		t.assigned_to = user.objects(username=d['assigned_to'])[0].id
		if not t.save():
			return JsonResponse({'success' : False}, status = 400)

	return JsonResponse({'success' : True}, status=200)