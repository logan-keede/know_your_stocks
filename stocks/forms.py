
from django import forms
from dhanhq import dhanhq
class UserForm(forms.Form):
    # resume_link = forms.URLField(label='resume_link', max_length=300)
    dhan_access = forms.CharField(max_length=300, required=True)
    dhan_client = forms.CharField(max_length=300, required=True)



class TradingOrderForm(forms.Form):
    TRANSACTION_CHOICES = (
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    )
    EXCHANGE_SEGMENT_CHOICES = (
        ('NSE', 'NSE'),
        ('FNO', 'FNO'),
        ('CUR', 'CUR'),
        ('BSE', 'BSE'),
        ('MCX', 'MCX'),
    )
    PRODUCT_TYPE_CHOICES = (
        ('CNC', 'CNC'),
        ('INTRA', 'INTRA'),
        ('MARGIN', 'MARGIN'),
        ('MTF', 'MTF'),
        ('CO', 'CO'),
        ('BO', 'BO'),
    )
    ORDER_TYPE_CHOICES = (
        ('LIMIT', 'LIMIT'),
        ('MARKET', 'MARKET'),
        ('SL', 'SL'),
        ('SLM', 'SLM'),
    )
    VALIDITY_CHOICES = (
        ('DAY', 'DAY'),
        ('IOC', 'IOC'),
    )
    AMO_TIME_CHOICES = (
        (None,None),
        ('OPEN', 'OPEN'),
        ('OPEN_30', 'OPEN_30'),
        ('OPEN_60', 'OPEN_60'),
    )
    TRANSACTION_TYPE = forms.ChoiceField(choices=TRANSACTION_CHOICES, required=True)
    EXCHANGE_SEGMENT = forms.ChoiceField(choices=EXCHANGE_SEGMENT_CHOICES, required=True)
    PRODUCT_TYPE = forms.ChoiceField(choices=PRODUCT_TYPE_CHOICES, required=True)
    ORDER_TYPE = forms.ChoiceField(choices=ORDER_TYPE_CHOICES, required=True)
    VALIDITY = forms.ChoiceField(choices=VALIDITY_CHOICES, required=True)
    SECURITY_ID = forms.CharField(max_length=100, required=True)
    QUANTITY = forms.IntegerField(required=True)
    DISCLOSED_QUANTITY = forms.IntegerField(required=False)
    PRICE = forms.FloatField(required=True)
    TRIGGER_PRICE = forms.FloatField(required=False)
    AFTER_MARKET_ORDER = forms.BooleanField(required=False)
    AMO_TIME = forms.ChoiceField(choices=AMO_TIME_CHOICES, required=False)
    BO_PROFIT_VALUE = forms.FloatField(required=False)
    BO_STOP_LOSS_VALUE = forms.FloatField(required=False)
    DRV_EXPIRY_DATE = forms.DateField(required=False)
    DRV_OPTIONS_TYPE = forms.ChoiceField(choices=((None,None),('CALL', 'CALL'), ('PUT', 'PUT')), required=False)
    DRV_STRIKE_PRICE = forms.FloatField(required=False)


class cancelForm(forms.Form):
    order_id = forms.CharField(max_length=300)