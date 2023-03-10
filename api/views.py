import time

import requests
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view

# Create your views here.
from rest_framework.response import Response

from api.serializer import historyserilizer
from index.models import historydata, profile, mtndataplan, glodataplan, mobile9dataplan, airteldataplan


def getusers(request, email, password):
    user = authenticate(request, username=email, password=password)
    if user:
        print('hello')
    else:
        return Response({'error': 'User credentials are not correct'})


@api_view(['GET'])
def buyairtime(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    number = request.GET.get('number')
    network = request.GET.get('network')
    amount = request.GET.get('amount')
    user = authenticate(request, username=email, password=password)
    if user:
        wallets = profile.objects.get(email=email)
        if int(amount) <= int(wallets.wallet):

            try:
                userid = "CK100357719"
                apikey = "8653N0QH286FP74414TYMA5VHKBNWR24O7QA91143LC05YQZ8713NI401YKKBPJ1"
                net = ''
                if network == '01':
                    net = "MTN"
                elif network == "02":
                    net = 'GLO'
                elif network == '03':
                    net = '9Mobile'
                elif network == '04':
                    net = 'Airtel'

                dat = requests.get(
                    "https://www.nellobytesystems.com/APIAirtimeV1.asp?UserID=" + userid + "&APIKey=" + apikey + "&MobileNetwork=" + network + "&Amount=" + amount + "&MobileNumber=" + number).json()
                istory = wallets.historydata_set.create(orderid=dat['orderid'],
                                                        statuscode=dat['statuscode'],
                                                        transaction_type='Airtime',
                                                        amount=amount, network=net, phonenumber=number,
                                                        )

                istory.save()

                balance = int(wallets.wallet) - int(amount)
                wallets.wallet = balance
                wallets.save()
                return Response({'success': 'Your request has been granted and will be processed'})



            except:
                return Response({'error': 'Error occur please try again later'})
        else:
            return Response({'error': 'Your wallet balance is too low for this transaction'})

    else:
        return Response({'error': 'Credentials are incorrect'})


def dataoption(request, networkname, wallets, data, phonenumber, network, ):
    plan = networkname.objects.get(value=data)
    getnetwork = ''
    if network == "01":
        getnetwork = "MTN"
    elif network == "02":
        getnetwork = "GLO"
    elif network == "03":
        getnetwork = "9MOBILE"
    elif network == "04":
        getnetwork = 'Airtel'
    if int(plan.dataprice) <= int(wallets.wallet):
        try:
            userid = "CK100357719"
            apikey = "8653N0QH286FP74414TYMA5VHKBNWR24O7QA91143LC05YQZ8713NI401YKKBPJ1"

            dat = requests.get(
                "https://www.nellobytesystems.com/APIDatabundleV1.asp?UserID=" + userid + "&APIKey=" + apikey + "&MobileNetwork=" + network + "&Dataplan=" + data + "&MobileNumber=" + phonenumber).json()
            istory = wallets.historydata_set.create(orderid=dat['orderid'],
                                                    statuscode=dat['statuscode'],
                                                    transaction_type='Data Plan',
                                                    amount=plan.dataprice, DataSize=plan.datagb,
                                                    phonenumber=phonenumber,
                                                    network=getnetwork, )

            istory.save()
            balance = int(wallets.wallet) - int(plan.dataprice)
            wallets.wallet = balance
            wallets.save()
            return Response({'success': "Your order has been received"})
        except:
            return Response({'error': "Error occur please try again later"})


    else:
        return Response({'error': 'Your wallet balance is too low for this transaction'})


@api_view(['GET'])
def buydata(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    network = request.GET.get('network')
    number = request.GET.get('number')
    data = request.GET.get('data')
    user = authenticate(request, username=email, password=password)
    if user:
        wallets = profile.objects.get(email=email)
        if network == "01":
            dataoption(request, mtndataplan, wallets, data, number)
        elif network == "02":
            dataoption(request, glodataplan, wallets, data, number)
        elif network == "03":
            dataoption(request, mobile9dataplan, wallets, data, number)
        elif network == "04":
            dataoption(request, airteldataplan, wallets, data, number)
    else:
        return Response({'error': 'Credentials are incorrect'})


@api_view(['GET'])
def base(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    user = authenticate(request, username=email, password=password)
    if user:

        pro = profile.objects.get(email=email)
        his = historydata.objects.filter(users=pro.id)
        total = his.count()
        serializer = historyserilizer(his, many=True)
        context = {'Total Transaction': total, 'history': serializer.data}
        return Response(context)
    else:
        return Response({'error': 'User credentials are not correct'})


@api_view(['GET'])
def buywaec(request):
    email = request.query_params['email']
    password = request.query_params['password']
    user = authenticate(request, username=email, password=password)
    if user:
        pass


@api_view(['GET'])
def historydatas(request, pk):
    email = request.GET.get('email')
    password = request.GET.get('password')
    user = authenticate(request, username=email, password=password)
    if user:

        his = historydata.objects.get(id=pk)
        serializer = historyserilizer(his, many=False)
        return Response(serializer.data)
    else:
        return Response({'error': 'Credentials are incorrect'})


@api_view(['GET'])
def walletballance(request):
    username = request.GET.get('email')
    pas = request.GET.get('password')
    user = authenticate(request, username=username, password=pas)
    if user:
        gett = profile.objects.get(email=username)
        wallet = gett.wallet
        context = {'wallet balance': wallet}
        return Response(context)
    else:
        return Response({'Error': 'credentials are incorrect'})
