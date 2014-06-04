from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from all_data_view import align, align_filter
from home_view import IntervalList, int_filter
from detail_view import AlignDetailView
from interval_detail_view import IntervalDetailView
from graph_view import Graph_Form
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from views import LibraryListView 
from user_detail import UserDetailView
from comment_posted import comment_posted

""" urls.py link the regex of each webpage with the function that renders the view page. Named urls are used with name="" that can be used to redirect pages in the HTML Templates.
"""

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/', include(admin.site.urls)),

# page to show library information
                      url(r'^libs/$',LibraryListView.as_view(),name='librar_list'),
# Page to show all read alignments
                      url(r'^align/$',align,name="all_data"),                    
                      url(r'^(?P<pk>\d+)/align/$', AlignDetailView.as_view(), name='AlignDetailView'),
# home page with all miRNA interval information 
                      url(r'^interval/$',login_required(IntervalList.as_view()),name='interval'),
# individual pages of each miRNA interval
                      url(r'^(?P<pk>[0-9A-Za-z-_.//:]+)/interval/$', IntervalDetailView.as_view(), name='IntervalDetailView', ),
#Interval Search page
                      url(r'^interval/search/$',int_filter,name='int_filter'),\
# Aligned reads search page
                       url(r'^align/search/$',align_filter,name='align_filter'),
# Login page 
                       url(r'^login/$', 'django.contrib.auth.views.login',{'template_name':'loq/login.html'}, name='login'),
#logout page
                       url('^logout/$', 'django.contrib.auth.views.logout_then_login',name='logout'),
# to include favit pages for favouriting functionality
                       url(r'^favit/', include('favit.urls')),
# User Pages
                      url(r'^(?P<pk>\d+)/user/$', UserDetailView.as_view(), name='user', ),
# Comment posted page, redirects back to original page after submitting comment
url(r'^comments/posted/$', comment_posted,name='comment_posted' ),
# comment page
                      url(r'^comments/', include('django.contrib.comments.urls')),
# Read Distribution graph generator page
                      url(r'^graph/$',Graph_Form, name='graph_form'),
)
# Flat pages for about, license and help pages 
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
