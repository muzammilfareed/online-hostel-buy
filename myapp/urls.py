from django.contrib import admin
from django.urls import path, include
from myapp import views, edit_add

urlpatterns = [
    path('house_info_save/', views.house_info_save, name='house_info'),
    path('get_user_data/', views.get_user_data, name='get_user_data'),
    path('edit_add/<int:pk>', edit_add.edit_add, name='edit_add'),
    path('status_change/<int:pk>', edit_add.status_change, name='status_change'),
    path('bocked_status_change/<int:pk>', edit_add.bocked_status_change, name='bocked_status_change'),
    path('delete/<int:pk>', edit_add.delete, name='delete'),
    path('edit_home/<int:pk>', edit_add.edit_home, name='edit_home'),
    path('delete_image/', edit_add.delete_image, name='delete_image'),
    path('delete_video/', edit_add.delete_video, name='delete_video'),
]