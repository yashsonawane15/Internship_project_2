from django.urls import path, include
from . import views

input_patterns = [
	path('category', views.CategoryInsert),
	path('todo', views.todoInsert),
	path('user', views.UserInsert),
	path('status', views.StatusInsert),
]

urlpatterns = [
	path('', views.index),
	path('success', views.SuccessView, name='success'),
	path('error', views.ErrorView, name='success'),
	path('input/', include(input_patterns) ),
	path('lists', views.listFetcher),
	path('display/<str:collection>', views.displayView),
	path('delete', views.DeleteDocument),
	path('modify', views.ModifyDocument),
]