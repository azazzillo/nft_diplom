from settings.celery import app
from django.db.models import F

from .models import Auction

@app.task
def do_test(auc_id: int,*args, **kwargs):
    Auction.objects.all().update(
        starting_bid = F('starting_bid' + 1)
    )
    print('OK')
