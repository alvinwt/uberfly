from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_tables2 import RequestConfig, SingleTableMixin
from tables import UserTable, CommentTable, FavTable
from django.utils.decorators import method_decorator
from django.contrib.comments import Comment
from favit.models import Favorite


"""This file generates individual user page."""
class UserDetailView(DetailView):
    model= User

    ### Requires login and authorization that is provided in the admin interface
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDetailView,self).dispatch(*args, **kwargs)

    def get_table_data (self):
        table_data= UserTable(User.objects.filter(username=self.object.username))
        return table_data
    
    def get_table2(self):
        table_data2= CommentTable(Comment.objects.filter(user=self.object.pk))
        return table_data2

       
    def get_fav(self):
        fav_data= FavTable(Favorite.objects.filter(user=self.object.pk))
        return fav_data
     
    def get_context_data(self, **kwargs):
        context = super(UserDetailView,self).get_context_data(**kwargs)
        context['table2'] = self.get_table2()
        context['fav'] = self.get_fav()
        context['user_detail'] = self.get_table_data()
        return context 
