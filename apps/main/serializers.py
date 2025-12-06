from rest_framework import serializers

from .models import User, NFT, Block, CustomUser, Auction


class NFTSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    
    status_choices = (
        ('ACTIVE', 'Active'),
        ('SOLD', 'Sold')
    )
    
    status = serializers.ChoiceField(
        choices=status_choices
    )
    description = serializers.CharField()
    image = serializers.ImageField()



class NFTCreateSerializer(serializers.ModelSerializer):

    status = serializers.CharField(
        default = 'Active'
    )

    class Meta:
        model = NFT
        fields = [
            'title', 'status', 'description',
            'image'
        ]
        

class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = [
            'datetimecreated', 'hash_this',''
        ]


class CustomUserSerializer(serializers.Serializer):

    class Meta:
        model = CustomUser
        fields = [
            'name', 'username', 'date_created'
        ]


class AuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model=Auction
        fields = [
            'title',
            'nft',
            'starting_bid',
            'datetime_finish',
        ]


class AuctionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = [
            'title', 'nft', 'startig_bid', 'datetime_finish'
        ]



