import time
import uuid

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import UUIDField
from django.shortcuts import render, redirect

from index.models import profile, mtndataplan, glodataplan, mobile9dataplan, airteldataplan, waecprice, historydata, \
    Dstpackages, GOtvpackages, Startimespackages


def index(request):
    # info, created = profile.objects.get(username=request.user.username)
    # context = {"info": info}
    mtn = mtndataplan.objects.all()[:10]
    glo = glodataplan.objects.all()[:10]
    mobile9 = mobile9dataplan.objects.all()[:10]
    airtel = airteldataplan.objects.all()[:10]
    context = {'mtn': mtn, 'glo': glo, 'mobile': mobile9, 'airtel': airtel}
    return render(request, 'index/home.html', context)


# this method below is use to register user
def registration(request):
    if request.user.is_authenticated:
        return redirect('index:index')
    if request.method == "POST":
        name = request.POST.get('username')
        mail = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get("confirm_password")
        number = request.POST.get('number')
        gender = request.POST.get('gender')
        try:
            mail = profile.objects.get(email=mail)
        except:
            if password == confirm:
                get_pass = make_password(password)
                account = profile.objects.create(username=name, password=get_pass, email=mail, phone_number=number,
                                                 gender=gender)
                account.save()
                messages.success(request, 'Account created successfully,')
                user = authenticate(request, username=mail, password=password)

                if user:
                    return redirect("index:loging")

            else:
                messages.error(request, 'Password doesnt match ')
                return redirect("index:create")
        messages.error(request, 'User Already have an Account')

        # return redirect("index:create")

    return render(request, "index/registration.html")


@login_required(login_url="index:loging")
def fundwallet(request):
    wallets = profile.objects.get(username=request.user)
    context = {"wallet": wallets}

    return render(request, "index/fundwallet.html", context)


@login_required(login_url='index:loging')
def airtime(request):
    wallets = profile.objects.get(username=request.user)

    if request.method == 'POST':
        # http://shaww.pythonanywhere.com/

        phonenumber = request.POST.get('number')
        amount = request.POST.get('amount')
        network = request.POST.get('network')
        if int(amount) <= int(wallets.wallet):
            if request.user.is_authenticated:

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
                        "https://www.nellobytesystems.com/APIAirtimeV1.asp?UserID=" + userid + "&APIKey=" + apikey + "&MobileNetwork=" + network + "&Amount=" + amount + "&MobileNumber=" + phonenumber).json()
                    istory = request.user.historydata_set.create(orderid=dat['orderid'],
                                                                 statuscode=dat['statuscode'],
                                                                 transaction_type='Airtime',
                                                                 amount=amount, network=net, phonenumber=phonenumber,
                                                                 )

                    istory.save()

                    # amount = profile.objects.create(id=wallets.id,username=wallets.username, wallet=balance, email=wallets.email, pasword=wallets.pasword)
                    # amount.save()
                    balance = int(wallets.wallet) - int(amount)
                    wallets.wallet = balance
                    wallets.save()
                    messages.success(request, 'Your request has been granted and will be processed')

                    return redirect("index:airtime")

                except:
                    messages.error(request, 'Error occur please try again later')
        else:
            messages.error(request, 'Your wallet balance is too low for this transaction')
    context = {'wallet': wallets}

    return render(request, 'index/airtime.html', context)


def dataoption(request, dataname, wallets, data, phonenumber, net):
    plan = dataname.objects.get(value=data)
    getnetwork = ''
    if net == "01":
        getnetwork = "MTN"
    elif net == "02":
        getnetwork = "GLO"
    elif net == "03":
        getnetwork = "9MOBILE"
    elif net == "04":
        getnetwork = 'Airtel'
    if int(plan.dataprice) <= int(wallets.wallet):
        try:
            userid = "CK100357719"
            apikey = "8653N0QH286FP74414TYMA5VHKBNWR24O7QA91143LC05YQZ8713NI401YKKBPJ1"

            dat = requests.get(
                "https://www.nellobytesystems.com/APIDatabundleV1.asp?UserID=" + userid + "&APIKey=" + apikey + "&MobileNetwork=" + net + "&Dataplan=" + data + "&MobileNumber=" + phonenumber).json()
            istory = request.user.historydata_set.create(users=request.user, orderid=dat['orderid'],
                                                         statuscode=dat['statuscode'],
                                                         transaction_type='Data Plan',
                                                         amount=plan.dataprice, DataSize=plan.datagb,
                                                         phonenumber=phonenumber,
                                                         network=getnetwork, )

            istory.save()
            balance = int(wallets.wallet) - int(plan.dataprice)
            wallets.wallet = balance
            wallets.save()
            messages.success(request, "Your order has been received")
        except:
            messages.error(request, "Error occur please try again later")


    else:
        messages.error(request, 'Your wallet balance is too low for this transaction')


@login_required(login_url='index:loging')
def dataplan(request):
    wallets = profile.objects.get(username=request.user)
    mtn = mtndataplan.objects.all()
    glo = glodataplan.objects.all()
    mobile9 = mobile9dataplan.objects.all()
    airtel = airteldataplan.objects.all()

    if request.method == "POST":
        net = request.POST.get('network')
        phonenumber = request.POST.get('number')
        data = request.POST.get('plan')

        if net == "01":
            dataoption(request, mtndataplan, wallets, data, phonenumber, net)
        elif net == "02":
            dataoption(request, glodataplan, wallets, data, phonenumber, net)
        elif net == "03":
            dataoption(request, mobile9dataplan, wallets, data, phonenumber, net)
        elif net == "04":
            dataoption(request, airteldataplan, wallets, data, phonenumber, net)

    context = {'wallet': wallets, 'mtn': mtn, 'glo': glo, "mobile9": mobile9, "airtel": airtel}
    return render(request, 'index/data.html', context)


@login_required(login_url="index:loging")
def profiles(request):
    pro = profile.objects.get(username=request.user)
    context = {'profile': pro}
    return render(request, 'index/profile.html', context)


@login_required(login_url="index:loging")
def updateprofile(request):
    pro = profile.objects.get(username=request.user)

    if request.method == 'POST':
        user = request.POST.get('username')
        gender = request.POST.get('gender')
        mail = request.POST.get('email')
        number = request.POST.get('number')

        pro.gender = gender
        pro.email = mail
        pro.phone_number = number
        pro.username = user
        pro.save()
        messages.success(request, "Profile updated successfully")
        return redirect("index:profile")

    context = {"profile": pro}
    return render(request, 'index/updateprofile.html', context)


@login_required(login_url='index:loging')
def waec(request):
    form = request.POST.get("waec")
    wallets = profile.objects.get(username=request.user)
    waec = waecprice.objects.all()

    if request.method == "POST":
        wa = waecprice.objects.get(value=form)
        num = request.POST.get('number')
        examtype = request.POST.get('waec')
        getwaec = ""

        if int(wa.price) <= int(wallets.wallet):

            try:

                userid = "CK100357719"
                apikey = "8653N0QH286FP74414TYMA5VHKBNWR24O7QA91143LC05YQZ8713NI401YKKBPJ1"
                if examtype == "waec-registration":
                    getwaec = "Waec Registration Pin"
                else:
                    getwaec = "Waec Result Checker Pin"

                data = requests.get(
                    'https://www.nellobytesystems.com/APIWAECV1.asp?UserID=' + userid + '&APIKey=' + apikey + '&ExamType=' + examtype + '&PhoneNo=' + num).json()
                istory = request.user.historydata_set.create(orderid=data['orderid'],
                                                             statuscode=data['statuscode'],
                                                             transaction_type='Waec E-pin',
                                                             amount=wa.price, product=getwaec, phonenumber=num,
                                                             )

                istory.save()

                balance = int(wallets.wallet) - int(wa.price)
                wallets.wallet = balance
                wallets.save()
                messages.success(request, "Your order has been received")
            except:
                messages.error(request, "Error occur please try again later")
        else:
            messages.error(request, 'Your wallet ballance is not sufficients for this transaction')

    context = {"wallet": wallets, 'waec': waec}
    return render(request, 'index/waec.html', context)


def loging(request):
    if request.user.is_authenticated:
        return redirect('index:index')
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("index:index")
        else:
            messages.error(request, "Email or password is incorrect")

    return render(request, 'index/loging.html')


@login_required(login_url="index:loging")
def print(request):
    wallets = profile.objects.get(username=request.user)
    context = {"wallet": wallets}
    if request.method == "POST":

        quantity = request.POST.get("quantity")
        network = request.POST.get("network")
        amount = request.POST.get("amount")
        discount = int(amount) * int(quantity)

        if int(discount) <= int(wallets.wallet):
            try:
                userid = "CK100357719"
                apikey = "8653N0QH286FP74414TYMA5VHKBNWR24O7QA91143LC05YQZ8713NI401YKKBPJ1"

                data = requests.get(
                    'https://www.nellobytesystems.com/APIEPINV1.asp?UserID=' + userid + '&APIKey=' + apikey + '&MobileNetwork=' + network + '&Value=' + amount + '&Quantity=' + quantity).json()
                istory = request.user.historydata_set.create(users=request.user, orderid=data['orderid'],
                                                             statuscode=data['statuscode'],
                                                             transaction_type='airtime Printing',
                                                             amount=data, )

                istory.save()
                wallets.wallet = wallets.wallet - discount
                wallets.save()
                messages.success(request, 'Recharge card printed successfully')
            except:
                messages.error(request, "Error occur please try again later")
        else:
            messages.error(request, "Your wallet balance is too low for this Transaction")

    return render(request, "index/printcard.html", context)


@login_required(login_url="index:loging")
def electricity(request):
    wallet = profile.objects.get(username=request.user)
    if request.method == 'POST':
        company = request.POST.get('company')
        meter = request.POST.get('meter')
        meter_number = request.POST.get('meter_number')
        phone_number = request.POST.get("phone_number")
        amount = request.POST.get('amount')
        if int(amount) <= int(wallet.wallet):
            try:
                userid = "CK100357719"
                apikey = "8653N0QH286FP74414TYMA5VHKBNWR24O7QA91143LC05YQZ8713NI401YKKBPJ1"
                getmeter = ''
                if meter == '01':
                    getmeter = 'PrePaid'
                else:
                    getmeter = 'PostPaid'
                data = requests.get(
                    'https://www.nellobytesystems.com/APIEPINV1.asp?UserID=' + userid + '&APIKey=' + apikey + '&ElectricCompany=' + company + '&MeterType=' + meter + '&MeterNo=' + meter_number + '&Amount=' + amount + 'PhoneNo=' + phone_number).json()
                istory = request.user.historydata_set.create(orderid=data['orderid'],
                                                             statuscode=data['statuscode'],
                                                             transaction_type='Electricity Payment',
                                                             amount=amount, metertype=getmeter,
                                                             meternumber=meter_number,
                                                             phone_number=phone_number, metertoken=data['metertoken'])

                istory.save()
                wallet.wallet = wallet.wallet - int(amount)
                wallet.save()
                messages.success(request, 'Recharge card printed successfully')

            except:
                messages.error(request, 'Error occur please try again')
        else:
            messages.error(request, 'Your wallet balance is too low for this transaction')

    context = {'wallet': wallet}
    return render(request, 'index/electricitybill.html', context)


def logoutpage(requst):
    logout(requst)
    return redirect('index:loging')


@login_required(login_url="index:loging")
def confirmpayment(request):
    wallet = profile.objects.get(username=request.user)

    context = {"wallet": wallet}
    return render(request, "index/confirm_payment.html", context)


@login_required(login_url="index:loging")
def payment(request):
    wallet = profile.objects.get(username=request.user)
    wallet.wallet = wallet.wallet + wallet.credit
    wallet.pending_wallet = 0.00
    wallet.display = 0.00
    wallet.pending_wallet = 0.00
    wallet.credit = 0.00
    wallet.save()
    messages.success(request, 'Payment made successfully')
    return redirect("index:fund")


@login_required(login_url="index:loging")
def pendigwallet(request):
    wallet = profile.objects.get(username=request.user)

    if request.method == 'POST':
        fund = request.POST.get("amount")

        percentage = 1.6 / 100
        percentage = percentage * int(fund)
        percentage = float(fund) - percentage
        funds = int(fund) * 100
        wallet.display = fund

        wallet.pending_wallet = funds
        wallet.credit = percentage
        wallet.save()

    return redirect('index:confirm-payment', )


@login_required(login_url='index:loging')
def cabletv(request):
    wallet = profile.objects.get(username=request.user)
    dstv = Dstpackages.objects.all()
    gotv = GOtvpackages.objects.all()
    startimes = Startimespackages.objects.all()
    # if request.method=='POST':
    #     number=request.POSt.get('')
    context = {"wallet": wallet, 'dstv': dstv, 'gotv': gotv, 'startimes': startimes, }
    return render(request, 'index/cableTv.html', context)


@login_required(login_url='index:loging')
def history(request):
    history = request.user.historydata_set.all()
    context = {'history': history}
    return render(request, 'index/History.html', context)


def singleHistory(request, pk):
    try:
        history = historydata.objects.get(id=pk)
    except:
        return redirect('index:history')

    try:
        userid = "CK100357719"
        apikey = "8653N0QH286FP74414TYMA5VHKBNWR24O7QA91143LC05YQZ8713NI401YKKBPJ1"
        data = requests.get(
            'https://www.nellobytesystems.com/APIQueryV1.asp?UserID=' + userid + '&APIKey=' + apikey + '&OrderID=' + history.orderid).json()

    except:
        messages.error(request, 'Error occur please try again later')
        return redirect('index:history')
    orderid = data['orderid']
    statuscode = data['statuscode']
    status = data['status']

    context = {"history": history, 'orderid': orderid, 'statuscode': statuscode, 'status': status}

    return render(request, 'index/singleHistory.html', context)


def get_secure_pass(request):
    mail = request.POST.get('email')
    if request.method == 'POST':
        try:
            secure = profile.objects.get(email=mail)
        except:
            messages.error(request, 'Invalid Email Address')
            return redirect('index:secure_pass')
        uudi = str(uuid.uuid4())[:7]
        secure.secure_pass = uudi
        secure.save()
        messages.info(request, 'Secure pass has been sent to your Email')
        return redirect('index:confirm_secure_pass')

    return render(request, 'index/get_securepass.html')


def change_password(request):
    mail = request.POST.get('email')
    se = request.POST.get('secure')
    pas = request.POST.get('password')
    if request.method == 'POST':
        try:
            secure = profile.objects.get(email=mail)
        except:
            messages.error(request, 'Invalid Secure Pass')
            return redirect('index:confirm_secure_pass')

        if se == secure.secure_pass and secure.secure_pass:
            secure.password = make_password(pas)

            secure.secure_pass = ''
            secure.save()
            messages.success(request, 'Password changed successfully')
            return redirect('index:loging')
        else:
            messages.error(request, 'Incorrect secure pass')

    return render(request, 'index/confirm_secure_pass.html')
