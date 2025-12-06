from rest_framework import serializers

from .models import Auction, Bid


class AuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = [
            'title', 'owner'
        ]

#  title = models.CharField(
#         max_length=220,
#         verbose_name='заголовок'
#     )
#     nft = models.ForeignKey(
#         to=NFT,
#         on_delete=models.CASCADE,
#         verbose_name='нфт_на_аукционе'
#     )
#     owner = models.ForeignKey(
#         to=CustomUser,
#         on_delete=models.CASCADE,
#         verbose_name='владелец_аукциона',
#         related_name='аукцион_владелец'
#     )
#     starting_bid = models.FloatField(
#         verbose_name='начальная ставка'
#     )
#     current_bid = models.FloatField(
#         verbose_name='текущая ставка',
#         blank=True
#     )
#     active = models.BooleanField(
#         default=True
#     )
#     datetime_created = models.DateTimeField(
#         verbose_name='дата начала аукциона',
#         default = datetime.datetime.now()
#     )
#     datetime_finish = models.DateTimeField(
#         verbose_name='дата окончания аукциона'
#     )
#     winner = models.ForeignKey(
#         to=CustomUser,
#         default=None,
#         on_delete=models.CASCADE,
#         verbose_name='победитель',
#         related_name='аукцион_победитель',
#         blank=True
#     )

#     # @property
#     # def duration(self):
#     #     return self.datetime_finish - self.datetime_created

#     class Meta:
#         verbose_name = 'Аукцион'
#         verbose_name_plural = 'Аукционы'

#     def __str__(self) -> str:
#         return \
#              f'{self.title} | {self.owner} | current_bid: {self.current_bid} | {self.datetime_finish}'



class AuctionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = [
            'title', 'nft', 'startig_bid', 'datetime_finish'
        ]
