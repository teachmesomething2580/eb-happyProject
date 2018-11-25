from django.db import models


class CashManager(models.Manager):
    def create(self, *args, **kwargs):
        from .models import Cash
        cash = Cash.give_point(**kwargs)
        return cash
