from django.urls import path

from webapp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('project_index/', views.ProjectView.as_view(), name='project_index'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_view'),
    path('project/<int:pk>/update', views.ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', views.DeleteProjectView.as_view(), name='project_delete'),
    path('project/<int:pk>/confirm_delete_object/', views.DeleteProjectView.as_view(), name='confirm_delete_project'),
    path('project/add/', views.ProjectAdd.as_view(), name='project_add'),
    path('tracker/<int:pk>/', views.TrackerDetail.as_view(), name='tracker_view'),
    path('tracker/add_view/<int:pk>/', views.TrackerAdd.as_view(), name='add_view'),
    path('tracker/<int:pk>/update', views.TrackerUpdateView.as_view(), name='tracker_update'),
    path('tracker/<int:pk>/delete/', views.DeleteTrackerView.as_view(), name='tracker_delete'),
    path('tracker/<int:pk>/confirm_delete/', views.DeleteTrackerView.as_view(), name='confirm_delete'),
]
