from settings.celery import app
from django.db.models import F

from .models import Auction, NFT

@app.task
def do_test(*args, **kwargs):
    Auction
    print('OK')
