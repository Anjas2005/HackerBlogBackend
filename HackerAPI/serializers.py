from rest_framework import serializers
from .models import BestNews

class Best_News_Serializer(serializers.ModelSerializer):
    Rank= serializers.IntegerField(required=True)
    class Meta:
        model=BestNews
        # fields=['Rank','Title','Link_To_Article','Points','Author','Post_Time']
        fields='__all__'
        extra_kwargs={
            "Rank":{"Validators":[]}
        }
