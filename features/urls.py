from django.conf.urls import url
from features import views

urlpatterns = [
    url(r'^$', views.FeatureListView.as_view(), name='feature_list'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^feature/(?P<pk>\d+)$', views.FeatureDetailView.as_view(), name='feature_detail'),
    url(r'^feature/new/$', views.CreateFeatureView.as_view(), name='feature_new'),
    url(r'^feature/(?P<pk>\d+)/edit/$', views.FeatureUpdateView.as_view(), name='feature_edit'),
    url(r'^feature/(?P<pk>\d+)/remove/$', views.FeatureDeleteView.as_view(), name='feature_remove'),
    url(r'^drafts/$', views.DraftListView.as_view(), name='feature_draft_list'),
    url(r'^feature/(?P<pk>\d+)/comment/$', views.add_comment_to_feature, name='add_comment_to_feature'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name= 'comment_remove'),
    url(r'feature/(?P<pk>\d+)/publish/$', views.feature_publish, name= 'feature_publish'),
]
