from django.urls import path
from .import views


urlpatterns=[
    path('',views.loginview,name='loginview'),
    path('profile/',views.profile, name='profile'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('document/',views.document,name='document'),
    path('viewdoc/',views.view_doc,name='viewdoc'),
    path('download/<int:document_id>/', views.download, name='download'),
    path('delete/<int:document_id>/',views.delete,name='delete'),
    path('upload/',views.upload,name='upload'),
    path('viewimg/',views.viewimg,name='viewimg'),
    path('images/delete/<int:imgid>/', views.delete_image, name='delete_image'),
    path('upload-text-to-pdf/', views.upload_and_convert_view, name='upload_text_to_pdf'),
    
]