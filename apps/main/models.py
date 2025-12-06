# Django
from typing import Any
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db.models import Manager
from django.utils import timezone
from django.db import models

# Python
import datetime
import hashlib
import json

class CustomUserManager(models.Manager):
    def create(self, **kwargs: Any) -> Any:
        return super().create(**kwargs)
    

class CustomUser(AbstractUser):

    name = models.CharField(
        verbose_name='имя',
        max_length=50,
        null=True,
        default='Unnamed'
    )
    date_created = models.DateField(
        verbose_name='дата создания',
        default=timezone.now
    )
    avatar = models.ImageField(
        verbose_name='аватар',
        upload_to='avatars/',
        default='avatars/no_ava.png'
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self) -> str:
        return f'{self.name} | {self.username} | {self.date_created}'

class NftCollection(models.Model):

    name=models.CharField(
        verbose_name='название',
        max_length=120
    )
    description=models.CharField(
        verbose_name='описание',
        max_length=250,
        default='Cool NFT'
    )
    owner=models.ForeignKey(
        verbose_name='владелец',
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='коллекция'
    )
    datetime_created=models.DateField(
        verbose_name='дата',
        default=timezone.now
    )

    class Meta:
        verbose_name='коллекция'
        verbose_name_plural='коллекции'
    
    def __str__(self) -> str:
        return f'{self.name} | {self.owner.name} | {self.datetime_created}'



class NFT(models.Model):
    
    active_choices = [
        ("ACTIVE", "Active"),
        ("FINISHED", "Finished"),
    ]
    status = models.CharField(
        max_length=20,
        choices=active_choices,
        verbose_name='статус',
        default='Active'
    )
    title = models.CharField(
        verbose_name='название',
        max_length=120,
    )
    description = models.CharField(
        verbose_name='описание',
        max_length=1000
    )
    token = models.CharField(
        verbose_name='токен',
        max_length=200
    )
    like = models.IntegerField(
        verbose_name='лайк',
        default=0
    )
    image = models.ImageField(
        verbose_name='картинка',
        upload_to='apps/main/static/img/'
    )
    collection=models.ForeignKey(
        verbose_name='Коллекция',
        related_name='нфт',
        to=NftCollection,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'нфт'
        verbose_name_plural = 'нфт'

    def __str__(self) -> str:
        return f'{self.title} | {self.status}'



class Transaction(models.Model):

    nft = models.ForeignKey(
        to=NFT,
        verbose_name='НФТ',
        related_name='НФТ_в_транзакции',
        on_delete=models.CASCADE
    )
    user_buyer = models.ForeignKey(
        to=CustomUser,
        verbose_name='покупатель',
        related_name='покупатель_в_транзакции',
        on_delete=models.CASCADE
    )
    user_saler = models.ForeignKey(
        to=CustomUser,
        verbose_name='продавец',
        related_name='продавец_в_транзакции',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=11,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'транзакция'
        verbose_name_plural = 'транзакции'

    def __str__(self) -> str:
        return f'{self.nft.title} | {self.user_buyer.name} | {self.price}'




class Coment(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='комментарий_автор',
        verbose_name='автор'
    )
    nft = models.ForeignKey(
        to=NFT,
        on_delete=models.CASCADE,
        related_name='нфт_коммент',
        verbose_name='нфт'
    )
    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self) -> str:
        return f'{self.nft.title} | {self.user.name} | '




# class NFTBlock(models.Model):

#     token=models.CharField(
#         verbose_name='ТОКЕН',
#         max_length=200,
#         unique=True
#     )
#     nft=models.ForeignKey(
#         verbose_name='НФТ',
#         to=NFT,
#         on_delete=models.CASCADE,
#         related_name='нфт_фореин'
#     )
#     datetime_created=models.DateTimeField(
#         verbose_name='дата',
#         default=datetime.datetime.now()
#     )


#     class Meta:
#         verbose_name='БЛОК'
#         verbose_name_plural='БЛОКИ'

#     def __str__(self) -> str:
#         return f'{self.nft.title} | {self.token}'


class BlockManager(models.Manager):
    
    def clean(
        self,
        *args,
        **kwargs
    ) -> 'Block':
        print('manager')
        if self.pk == 0:
            self.last_hash = '000000000000000000'
        else:
            self.last_hash = Block.objects.get(id=(int(self.pk) - 1)).hash_this
        return super().clean(*args, **kwargs)


class Block(models.Model):

    datetime_created = models.DateTimeField(
        verbose_name='дата создания',
        default=datetime.datetime.now()
    )
    data = models.ForeignKey(
        to=Transaction,
        verbose_name='инфа',
        related_name='транзакция',
        on_delete=models.CASCADE
    )
    last_hash = models.CharField(
        null=True,
        verbose_name='предыдущий хэш',
        max_length=200
    )

    @property
    def hash_this(self) -> str:
        
        h  = hashlib.sha256(str(self.pk) + str(self.datetime_created) \
                            + str(self.last_hash) + str(self.data.user_buyer) \
                            + str(self.data.user_saler) + str(self.data.price))
        return h
        
    objects = BlockManager()


    class Meta:
        verbose_name = 'блок'
        verbose_name_plural = 'блокчейн'

    def __str__(self) -> str:
        return f'{self.datetime_created}'



class Auction(models.Model):
    title = models.CharField(
        max_length=220,
        verbose_name='заголовок'
    )
    nft = models.ForeignKey(
        to=NFT,
        on_delete=models.CASCADE,
        verbose_name='нфт_на_аукционе'
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name='владелец_аукциона',
        related_name='аукцион_владелец'
    )
    starting_bid = models.FloatField(
        verbose_name='начальная ставка'
    )
    active = models.BooleanField(
        default=True
    )
    datetime_created = models.DateTimeField(
        verbose_name='дата начала аукциона',
        default = datetime.datetime.now()
    )
    datetime_finish = models.DateTimeField(
        verbose_name='дата окончания аукциона'
    )


    # @property
    # def duration(self):
    #     return self.datetime_finish - self.datetime_created

    class Meta:
        verbose_name = 'Аукцион'
        verbose_name_plural = 'Аукционы'

    def __str__(self) -> str:
        return \
             f'{self.title} | {self.owner} | {self.datetime_finish}'


class BidManager(models.Manager):
    def current(self, auction):
        return super().get_queryset().filter(auction=auction).order_by('-created_at')


class Bid(models.Model):
    auction = models.ForeignKey(
        to=Auction,
        on_delete = models.CASCADE,
        verbose_name='аукицон',
        related_name='ставка_на_аукцион'
    )
    who = models.ForeignKey(
        to=CustomUser,
        on_delete= models.CASCADE,
        verbose_name='юзер',
        related_name='ставка'
    )
    amount = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name='деньги'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    objects = BidManager()

    class Meta():
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'

    def __str__(self) -> str:
        return f'{self.who.name} | {self.amount} | {self.created_at}'
    



