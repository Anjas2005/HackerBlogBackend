from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.viewsets import ReadOnlyModelViewSet
import math

from .models import BestNews
from .serializers import Best_News_Serializer


class Best_News(generics.GenericAPIView):
    queryset= BestNews.objects.all()
    serializer_class = Best_News_Serializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data,many=True)
        if serializer.is_valid() :
            BestNews.objects.bulk_create(
                [BestNews(**data) for data in serializer.validated_data],
                update_conflicts=True,
                update_fields=["Title","Link_To_Article","Points","Author","Post_Time"],
                unique_fields=["Rank"],
                )
            return Response({"status":"Success", "data":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail","message": serializer.errors})
        
class Post_Best_News(ReadOnlyModelViewSet):
    queryset = BestNews.objects.all()
    serializer_class=Best_News_Serializer


