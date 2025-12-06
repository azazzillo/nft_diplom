from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

# from celery.execute import apply_async

from .models import Auction, Bid
from .serializers import AuctionSerializer, AuctionCreateSerializer
from .tasks import do_test

class AuctionViewSet(viewsets.ViewSet):
    queryset = Auction.objects.all()

    def list(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        serializer: AuctionSerializer = \
        AuctionSerializer(
            instance=self.queryset,
            many=True
        )
        return render(
            request=request,
            template_name='auctions.html',
            context={
                'auctions': serializer.data
            }
        )


    def create(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        serializer: AuctionCreateSerializer = \
            AuctionCreateSerializer(
                data=request.data
            )
        serializer.is_valid(
            raise_exception=True
        )
        auction: Auction = serializer.save()

        return Response(
            f'Auction {auction.title} was created'
        )


    @action(
        methods=['GET'],
        detail=False,
        url_path='auction/timer/(?P<pk>[^/.]+)'
    )
    def auction_timer(
        self,
        request: Request,
        pk: int = None
    ) -> Response: 
       do_test.apply_async(
           kwargs={'id':pk}, coutdown = 30
       )
       return Response(
           data={
               'message': 'ok'
           }
       )