from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('index/',views.index,name="index"),
    path('create/', views.create, name="create"),
    path('sell/<bpk>',views.sell,name="sell"),
    path('book/',views.book,name="book"),
    path('mybook/',views.mybook,name="mybook"),
    path('upbook/',views.upbook,name="upbook"),
    path('update/<bpk>', views.update, name="update"),
    path('cancle/<bpk>',views.cancle,name="cancle"),
    path('tcancle/<bpk>',views.tcancle,name="tcancle"),
    path('mysell/',views.mysell,name="mysell"),
    
    path('deposit',views.deposit, name='deposit'),
    
    path('request-deposit', views.requestDeposit, name='requestDeposit'),
    path('confirm-deposit', views.confirmDeposit, name='confirmDeposit'),

    path('request-refund', views.requestRefund, name='requestRefund'),
    path('confirm-refund', views.confirmRefund, name='confirmRefund'),
]