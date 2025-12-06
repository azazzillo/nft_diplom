# Django
from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

# DRF
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.request import Request

# Python
from web3 import Web3, HTTPProvider
from typing import Optional
import json

# Local
from .serializers import (NFTSerializer, NFTCreateSerializer, 
                        BlockSerializer, AuctionSerializer)

from .models import NFT, Block, CustomUser, NftCollection, Auction
from .forms import NFTForm, NFTCollectioForm,AuctionForm

from eth_account import Account
import logging
from eth_account.messages import encode_defunct

api_key = "https://practical-neat-dust.quiknode.pro/ff39da76a81be4583485205f863311521a9bcae1/"

# logger = logging.getLogger(__name__)



class NftViewSet(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]
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
        nfts = self.queryset
        print(nfts)

        return render(
            request=request,
            template_name='main/nfts.html',
            context={
                'nfts': nfts
            }
        )


def auc(request, auc_id: int):
    if request.method == 'GET':
        auc = Auction.objects.get(id=auc_id)
        return render(
            request=request,
            template_name='main/ret.html',
            context={
                'auction':auc
            }
        )



def new_auction(request):
    form=AuctionForm()
    if request.method=='POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            auction=form.save(commit=False)
            auction.owner = request.user
            auction.save()

            return render(
                request=request,
                template_name='main/create_auction.html',
                context={
                    'message':'Auction started',
                    'form':form
                }
            )
        form = AuctionForm()

        return render(
            request=request,
            template_name='main/create_auction.html',
            context={
                'message':'',
                'form':form
            }
        )
    
    form = AuctionForm()
    return render(
            request=request,
            template_name='main/create_auction.html',
            context={
                'message':'start your own auction',
                'form':form
            }
        )


# class CreateViewSet(viewsets.ViewSet):
#     def list(
#         self,
#         request: Request,
#         *args,
#         **kwargs
#     ) -> Response:
#         form = NFTForm
#         return render(
#             request=request,
#             template_name='main/create_nft.html',
#             context={
#                 'form':form,
#                 'message':''
#             }
#         )

def create_nft(request:Request) -> Response:
    form=NFTForm()
    if request.method == "POST":
        form = NFTForm(request.POST, request.FILES)
        print(request)
        if not form.is_valid():
            print(form.errors)
            print(form.cleaned_data)
        if form.is_valid():
            print('is_valid')
            nft=form.save(commit=False)
            nft.like=0
            nft.status='Active'
            nft.save()
            
            return render(
                request=request,
                template_name='main/create_nft.html',
                context={
                    'form':form,
                    'message':f'New NFT {nft.title} created succesfully'
                }
            )
        else:
            form = NFTForm()
        
            print(form.is_valid())
            return render(
                request=request,
                template_name='main/create_nft.html',
                context={
                    'form':form,
                    'message':''
                }
            )
    print(form.is_valid())
    return render(
        request=request,
        template_name='main/create_nft.html',
        context={
            'form': form,
            'message':'Add new NFT!!'
        }
    )


class NftMainPageViewSet(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]
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
        print('here !@@!K@!L!K#:')
        nfts = serializer.data
        return render(
            request=request,
            template_name='main/index.html',
            context={
                'nfts': nfts
            }
        )


    # def retrieve(
    #     self,
    #     request: Request,
    #     pk: Optional[int] = None
    # ) -> Response:
    #     nft = self.queryset.filter(id=pk)
    #     serializer: NFTSerializer = \
    #         NFTSerializer(instance=nft)
        
    #     return render(
    #         request=request,
    #         template_name='main/retrieve.html'
    #     )

    # def create(
    #     self,
    #     request: Request,
    #     *args: tuple,
    #     **kwargs: dict
    # ) -> Response:
    #     serializer: NFTCreateSerializer = \
    #         NFTCreateSerializer(
    #             data = request.data
    #         )
    #     serializer.is_valid(
    #         raise_exception=True
    #     )
    #     nft: NFT = serializer.save()

    #     return render(
    #         request=request,
    #         template_name='main/create_nft.html',
    #         context={
    #             'nft': serializer.data
    #         }
    #     )
    
    # def destory(
    #     self,
    #     request: Request,
    #     pk: str
    # ) -> Response:
    #     nft = self.queryset.get(id=pk)
    #     title: str = nft.title
    #     nft.delete()

    #     return Response(
    #         f'NFT {title} was deleted'
    #     )


def to_logout(
    request
):
    print('lsdlfosfoskf;sf;lsmflsm')
    logout(request=request)

    return redirect(
        '/reg/'
    )



class BlockView(viewsets.ViewSet):

    queryset = Block.objects.all()

    def list(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        serializer: BlockSerializer = \
            BlockSerializer(
                instance=self.queryset,
                many = True
            )
        
class ProfileViewSet(viewsets.ViewSet):
    permission_classes=[
        IsAuthenticated
    ]
    queryset=CustomUser.objects.all()
    def list(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict,
    ):
        print(request)
        user = CustomUser.objects.get(id=request.user.pk)
        print(user.id)

        return render(
            request=request,
            template_name='main/profile.html',
            context={
                'user':user
            }
        )

    # @action(method=['POST'],detail=False)
    # def change_avatar(
    #     self,
    #     request: Request,
    #     *args: tuple,
    #     **kwargs: dict
    # ):
    #     user = CustomUser.objects.get(id=request.id)
    #     avatar = 


def collection(request):
    form = NFTCollectioForm
    if request.method == 'POST':
        form = NFTCollectioForm(request.POST)
        if form.is_valid:
            collection = form.save(commit=False)
        
            collection.owner = request.user.id
            collection.save()
            return render(
                request=request,
                template_name='main/collection.html',
                context={
                    'form':form,
                    'collection': NftCollection.objects.get(owner=request.user.pk)
                }
            )

    return render(
        request=request,
        template_name='main/collection.html',
        context={
            'form': form,
            'collection': NftCollection.objects.get(owner=request.user.pk),
        }
    )


