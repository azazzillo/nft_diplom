from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action, api_view


from eth_account.messages import encode_defunct
from eth_account import Account

import json
from web3 import Web3, HTTPProvider

from .serializers import UserSerializer
from .models import CustomUser


api_key = "https://practical-neat-dust.quiknode.pro/ff39da76a81be4583485205f863311521a9bcae1/"

# class NftViewSet(viewsets.ViewSet):

#     queryset = NFT.objects.all()
    
#     def list(
#         self,
#         request: Request,
#         *args: tuple,
#         **kwargs: dict
#     ) -> Response:
#         serializer: NFTSerializer = \
#             NFTSerializer(
#                 instance=self.queryset,
#                 many=True
#             )

#         return render(
#             request=request,
#             template_name='main/index.html',
#             context={
#                 'nfts':serializer.data
#             }

class LoginRegisterViewSet(viewsets.ViewSet):

    permission_classes = [
        
    ]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def list(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        # print(request.user)
        if request.user.is_authenticated:
            return redirect('/main/main')
        return render(
            request=request,
            template_name='main/login.html'
        )


@csrf_exempt 
def to_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        wallet_address = data.get('wallet_address')
        user = CustomUser.objects.filter(username=wallet_address).first()

        if user:
            authenticate(request, username=wallet_address)
            login(request, user)
            return redirect(
                '/main/main'
            ) 
        new_user = CustomUser.objects.create(username=wallet_address)
        authenticate(request, username=wallet_address)
        login(request, new_user)
        return redirect(
            '/main/main'
        )  

    print('heelo the end of func')

    return redirect(
        '/reg/'
    ) 

