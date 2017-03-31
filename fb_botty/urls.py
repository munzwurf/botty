from django.conf.urls import include,url
from .views import MainView

urlpatterns= [
	url(r'^a6d16b993c7b5cfe9a8666dda5d1be64332f88dcac2a2f4ed4/?$', MainView.as_view()),
]

