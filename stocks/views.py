from django.shortcuts import render
from dhanhq import dhanhq, marketfeed
# # Create your views here.
from .forms import UserForm, TradingOrderForm, cancelForm
from .models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from dhanhq import dhanhq
from django.shortcuts import redirect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.views.decorators.csrf import csrf_exempt
import json
# import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()




# df = pd.read_excel("mails.xlsx")



def send_mail(body, email):
    fromaddr = os.environ.get("SENDERMAIL")
    # toaddr = email
    msg = MIMEMultipart()
    
    msg['From'] = os.environ.get("SENDERMAIL")
    msg['To'] = email
    
    msg['Subject'] = "POSTBACK ALERT"
    
    body = str(body)
    
    msg.attach(MIMEText(body, 'plain'))

    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()

    # print(os.environ.get("SENDERPASS"))
    # Authentication
    smtpserver.login(fromaddr, os.environ.get("SENDERPASS"))
    
    # Converts the Multipart msg into a string
    text = msg.as_string()
    # sending the mail
    smtpserver.sendmail(fromaddr, email, text)
    
    # terminating the session
    smtpserver.close()

@login_required(login_url="/accounts/google/login")
def get_holdings(request):
    # if request.method == 'GET':
    if request.user.dhan_access == "blank" or request.user.dhan_client == "blank":  
        return redirect("/stocks/fill_form")
        # pass
    else:
        dhan = dhanhq(request.user.dhan_access,request.user.dhan_access)
        return JsonResponse(dhan.get_holdings())

@login_required(login_url="/accounts/google/login")
def place_buy_order(request):
    if request.method == 'POST':
        if request.user.dhan_access == "blank" or request.user.dhan_client == "blank":  
            return redirect("/stocks/fill_form/")
        else:
            form = TradingOrderForm(request.POST)
            if form.is_valid():
                # if form.is_valid():

                cleaned_data = form.cleaned_data
                
                dhan = dhanhq(request.user.dhan_access, request.user.dhan_access)
                # print(dhan.BUY)
                print(cleaned_data)
                TRANSACTION_CHOICES = {
                    'BUY': dhan.BUY,
                    'SELL': dhan.SELL,
                }

                EXCHANGE_SEGMENT_CHOICES = {
                    'NSE': dhan.NSE,
                    'FNO': dhan.FNO,
                    'CUR': dhan.CUR,
                    'BSE': dhan.BSE,
                    'MCX': dhan.MCX,
                }

                PRODUCT_TYPE_CHOICES = {
                    'CNC': dhan.CNC,
                    'INTRA': dhan.INTRA,
                    'MARGIN': dhan.MARGIN,
                    'MTF': dhan.MTF,
                    'CO': dhan.CO,
                    'BO': dhan.BO,
                }

                ORDER_TYPE_CHOICES = {
                    'LIMIT': dhan.LIMIT,
                    'MARKET': dhan.MARKET,
                    'SL': dhan.SL,
                    'SLM': dhan.SLM,
                }
                if cleaned_data["DRV_OPTIONS_TYPE"]=="":
                    cleaned_data["DRV_OPTIONS_TYPE"]=None
                try:
                    json_data = {
                        'tag': '',
                        'transaction_type': TRANSACTION_CHOICES[cleaned_data['TRANSACTION_TYPE']],
                        'exchange_segment': EXCHANGE_SEGMENT_CHOICES[cleaned_data['EXCHANGE_SEGMENT']],
                        'product_type': PRODUCT_TYPE_CHOICES[cleaned_data['PRODUCT_TYPE']],
                        'order_type': ORDER_TYPE_CHOICES[cleaned_data['ORDER_TYPE']],
                        'validity': cleaned_data['VALIDITY'],
                        'security_id': cleaned_data['SECURITY_ID'],
                        'quantity': cleaned_data['QUANTITY'],
                        'disclosed_quantity': cleaned_data.get('DISCLOSED_QUANTITY', 0),
                        'price': cleaned_data['PRICE'],
                        'trigger_price': cleaned_data.get('TRIGGER_PRICE', 0),
                        'after_market_order': cleaned_data.get('AFTER_MARKET_ORDER', False),
                        'amo_time': cleaned_data.get('AMO_TIME', ''),
                        'bo_profit_value': cleaned_data.get('BO_PROFIT_VALUE', 0),
                        'bo_stop_loss_value': cleaned_data.get('BO_STOP_LOSS_VALUE', 0),
                        'drv_expiry_date': cleaned_data.get('DRV_EXPIRY_DATE', None),
                        'drv_options_type': cleaned_data.get('DRV_OPTIONS_TYPE', None),
                        'drv_strike_price': cleaned_data.get('DRV_STRIKE_PRICE', None)
                    }
                    print(json_data)

                    response = dhan.place_order(
                        tag='',
                        transaction_type= TRANSACTION_CHOICES[cleaned_data['TRANSACTION_TYPE']],
                        exchange_segment=EXCHANGE_SEGMENT_CHOICES[cleaned_data['EXCHANGE_SEGMENT']],
                        product_type=PRODUCT_TYPE_CHOICES[cleaned_data['PRODUCT_TYPE']],
                        order_type=ORDER_TYPE_CHOICES[cleaned_data['ORDER_TYPE']],
                        validity=cleaned_data['VALIDITY'],
                        security_id=cleaned_data['SECURITY_ID'],
                        quantity=cleaned_data['QUANTITY'],
                        disclosed_quantity=cleaned_data.get('DISCLOSED_QUANTITY', 0),
                        price=cleaned_data['PRICE'],
                        trigger_price=cleaned_data.get('TRIGGER_PRICE', 0),
                        after_market_order=cleaned_data.get('AFTER_MARKET_ORDER', False),
                        amo_time=cleaned_data.get('AMO_TIME', ''),
                        bo_profit_value=cleaned_data.get('BO_PROFIT_VALUE', 0),
                        bo_stop_loss_Value=cleaned_data.get('BO_STOP_LOSS_VALUE', 0),
                        drv_expiry_date=cleaned_data.get('DRV_EXPIRY_DATE',None),
                        drv_options_type=cleaned_data.get('DRV_OPTIONS_TYPE',None),
                        drv_strike_price=cleaned_data.get('DRV_STRIKE_PRICE',None)
                    )
                    return JsonResponse(response)
                except:
                    return JsonResponse({"error":"some error occured"})
    else:
        return render(request, "order.html", {"form":TradingOrderForm})
    
@login_required(login_url="/accounts/google/login")
def get_trade_book(request):
    if request.user.dhan_access == "blank" or request.user.dhan_client == "blank":  
        return redirect("/stocks/fill_form/")
    dhan = dhanhq(request.user.dhan_access, request.user.dhan_access)
    response = dhan.get_trade_book()
    return JsonResponse(response)

@login_required(login_url="/accounts/google/login")
def get_order_list(request):
    if request.user.dhan_access == "blank" or request.user.dhan_client == "blank":  
        return redirect("/stocks/fill_form/")
    dhan = dhanhq(request.user.dhan_access, request.user.dhan_access)
    response = dhan.get_order_list()
    return JsonResponse(response)

@login_required(login_url="/accounts/google/login")
def cancel_order(request):
    if request.user.dhan_access == "blank" or request.user.dhan_client == "blank":  
        return redirect("/stocks/fill_form/")
    if request.method == 'POST':
        form = cancelForm(request.POST)
        if form.is_valid():
            dhan = dhanhq(request.user.dhan_access, request.user.dhan_access)
            order_id = form.cleaned_data["order_id"]
            response = dhan.cancel_order(order_id)
            return JsonResponse(response)
    else:
        return render(request,"cancel_order.html", {"form":cancelForm})
@login_required(login_url="/accounts/google/login")
def fill_form(request):
    if request.user.dhan_access == "blank" or request.user.dhan_client == "blank":  
        return redirect("/stocks/fill_form/")
    if request.method == 'POST':
        form = UserForm(request.POST)
        user_instance = User.objects.get(email=request.user.email)
        if form.is_valid():
            form = form.cleaned_data
            user_instance.dhan_access = form['dhan_access']
            user_instance.dhan_client = form['dhan_client']
            user_instance.save()
            return redirect("/stocks/get_holdings")
        else:
            return JsonResponse({'error': 'something wrong'}, status=400)
    else:  # GET request
        return render(request, 'fill_form.html', {'form':UserForm})

@csrf_exempt
def postback(request,id):
    if request.method == "POST":
        body = json.loads(request.body)
        user_instance = User.objects.get(id=id)
        user_email = user_instance.email
        send_mail(body, user_email)
        return JsonResponse({"status":"success"})