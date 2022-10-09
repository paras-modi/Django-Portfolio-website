


# Create your views here.

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from home.models import Person, Transaction
from home.paytm_checksum import generate_checksum, verify_checksum



from home.task import email_task
from me import settings


def Homepage(request):
    if request.method == "GET":
      return render(request, 'homepage.html')

def payment(request):
    #amount=200
    transaction = Transaction.objects.create()
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY
    print(transaction.id)
    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str("Unknown")),
        ('TXN_AMOUNT', str(200)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)



def Contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['number']
        message=request.POST['text']
       # print(name,email,phone,message)
        ins=Person(full_name=name,email=email,phone_number=phone,message=message)
        ins.save()
        try:
            subject= name +" has send you a message"
            #message1=message
            email_task.delay(subject,message)
            #email_from=settings.EMAIL_HOST_USER
            #recipient_list=['parasmodi100@gmail.com']
            #send_mail(subject,message1,email_from,recipient_list)
            print("successfull")
        except Exception as e:
            print(e)

        print("the data is saved")
    return render(request,'contact.html')

def resume(request):
    return render(request,'resume.html')

def projects(request):
    return render(request,'project.html')



