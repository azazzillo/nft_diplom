from django import forms
from django.utils.safestring import mark_safe

from .models import NFT, Auction, Bid,NftCollection


class NFTForm(forms.ModelForm):

    required_css_class='required-field'

    title=forms.CharField(widget=forms.TextInput(
        attrs={"class":"title-form"}
    ))
    description=forms.CharField(widget=forms.Textarea(
        attrs={"class":"description-form"}
    ))
    image=forms.ImageField(widget=forms.FileInput(
        attrs={"class":"image_in"}
    ))
    class Meta:
        model=NFT
        fields=[
            'title','description','image','collection'
        ]


class NFTCollectioForm(forms.ModelForm):

    class Meta:
        model=NftCollection
        fields=[
            'name','description'
        ]


class AuctionForm(forms.ModelForm):
    required_css_class='required-field'

    title=forms.CharField(widget=forms.TextInput(
        attrs={"class":"title-form"}
    ))
    description=forms.CharField(widget=forms.Textarea(
        attrs={"class":"description-form"}
    ))
    starting_bid=forms.FloatField(widget=forms.NumberInput)
    datetime_finish=forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'type':'datetime-local'}
    ))
    class Meta:
        model=Auction
        fields=[
            'title','nft','starting_bid','datetime_finish'
        ]


class FormSerializer(forms.ModelForm):

    class Meta:
        model=Bid
        fields=[
            'amount'
        ]
