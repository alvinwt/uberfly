from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from all_data_view import align, view, align_filter
from home_view import IntervalList, int_filter
from detail_view import AlignDetailView
from interval_detail_view import IntervalDetailView
from search_view import AlignViewSet, IntervalViewSet
from graph_view import Graph_Form
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required
from views import AlignListAPIView,LibraryListView, IntView,coordinate,showStaticImage, AlignListView
from django_filters.views import FilterView
from loq.models import Library, Interval
from user_detail import UserDetailView
from comment_posted import comment_posted
admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'alignview', AlignViewSet)
router.register(r'intview',IntervalViewSet)
urlpatterns = patterns('',
                       (r'^admin/', include(admin.site.urls)),                     
                      url(r'^id/$',LibraryListView.as_view(),name='library_list'),
                      url(r'^align/$',align,name="all_data"),                    
#                      url(r'^(?P<pk>\d+)/align/graph<pk>.png$',plotResults,name='graph'),
                      url(r'^(?P<pk>\d+)/align/$', AlignDetailView.as_view(), name='AlignDetailView'),
                      url(r'^api/$', AlignListAPIView.as_view(), name='list'),
                      url(r'^interval/$',login_required(IntervalList.as_view()),name='interval'),
                      url(r'^(?P<pk>[0-9A-Za-z-_.//:]+)/interval/$', IntervalDetailView.as_view(), name='IntervalDetailView', ),
# url(r'^(?P<pk>[0-9A-Za-z-_.//:]+)/interval/dist.png$', IntervalDetailView.get_dist, name='IntervalDetailViewDist', ),
                      url(r'^interval/search/$',int_filter,name='int_filter'),
                       url(r'^align/search/$',align_filter,name='align_filter'),
                       url(r'^login/$', 'django.contrib.auth.views.login',{'template_name':'loq/login.html'}, name='login'),
                       url('^logout/$', 'django.contrib.auth.views.logout_then_login',name='logout'),
                       url(r'^favit/', include('favit.urls')),
                      url(r'^(?P<pk>\d+)/user/$', UserDetailView.as_view(), name='user', ),
                       url(r'^comments/posted/$', comment_posted,name='comment_posted' ),
                      url(r'^comments/', include('django.contrib.comments.urls')),
                      url(r'^graph/$',Graph_Form, name='graph_form'),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^about-us/$', 'flatpage', {'url': '/about-us/'}, name='about'),
    url(r'^license/$', 'flatpage', {'url': '/license/'}, name='license'),
     url(r'^help/$', 'flatpage', {'url': '/help/'}, name='help'),
                        url(r'^',login_required(IntervalList.as_view()),name='home')
)

if settings.DEBUG:
    urlpatterns += patterns('',
                           (r'^debug/$','debug'),
     ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    # # patterns can be added tgt '+=' v useful for diff patterns
    # urlpatterns += patterns('',
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # (r'^lalign/$',AlignListView.as_view()),)
    # (r'^staticImage.png$', showStaticImage),
    #  url(r'^balign/$',plotResults),
