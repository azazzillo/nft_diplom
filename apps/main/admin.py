from django.contrib import admin

from main.models import (
    CustomUser,NFT,Transaction,
    Auction,Bid, Block, Coment,
    NftCollection
    )

admin.site.register(CustomUser)
admin.site.register(NFT)
admin.site.register(Transaction)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Block)
admin.site.register(Coment)
admin.site.register(NftCollection)
