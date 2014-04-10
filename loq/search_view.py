from loq.models import Library, Read_alignment, Interval
import rest_framework as rest
from rest_framework import serializers, viewsets, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'align': reverse('align-detail', request=request, format=format),
    })
class AlignSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True,view_name='align-detail')

    class Meta:
        model = Read_alignment
        fields = ('id','chr','start','stop','sequence',)
    
class AlignViewSet(viewsets.ReadOnlyModelViewSet):
    #queryset = Read_alignment.objects.all()
    model = Read_alignment
    serializer_class = AlignSerializer
    queryset = Read_alignment.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAdminUser]
    paginate_by = 10
    # def get_queryset(self):
    #     return self.request.Read_alignment.all()

    
class IntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interval
        
class IntervalViewSet(viewsets.ModelViewSet):
    model = Interval
    serializer_class = IntervalSerializer
    queryset = Interval.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAdminUser]
    paginate_by = 10
 
    
class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        
    
# class AlignRetrieveAPIView(RetrieveUpdateAPIView):
#     model = Read_alignment
#     serializer_class = AlignSerializer
