from django.http import HttpResponseRedirect
from loq.models import Interval
from django.contrib.comments.models import Comment

""" Comment_posted.py provides the link back to the original page after
submitting the comment. It transverse the comment table, to retreive the interval_id and uses get_absolute_url()
"""
def comment_posted( request ):
    if request.GET['c']:
        comment_id = request.GET['c']
        interval_id = Comment.objects.get(id=comment_id).content_object.pk
        post = Interval.objects.get(pk=interval_id)
        if post:
            return HttpResponseRedirect(post.get_absolute_url() )

    return HttpResponseRedirect( "/" )
