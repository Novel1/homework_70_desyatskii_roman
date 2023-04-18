from django.urls import path

from api.views import TrackerDetailView, TrackerDeleteView, TrackerUpdateView


urlpatterns = [
    path('tracker/<int:pk>/', TrackerDetailView.as_view(), name='detail_traker'),
    path('tracker/delete/<int:pk>/', TrackerDeleteView.as_view(), name='delete_tracker'),
    path('tracker/update/<int:pk>/', TrackerUpdateView.as_view(), name='update_tracker')
]