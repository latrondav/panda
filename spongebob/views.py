import email
from email import message
import imp
from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from samaritan import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . models import Contact, Bus
from . token import generate_token
from .forms import BookBusForm
from django.core.mail import EmailMessage, send_mail

# Create your views here.
#def home(request):
    #return HttpResponse("Hello World")

def home_page(request):
    busobj = Bus.objects.all()
    return render(request, 'index.html', {'Bus':busobj})

def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        

        try:
            remember = request.POST['remember-me']
            if remember:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        except:
            is_private = False
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True

        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "LOGGED IN SUCCESSFULLY!")
            busobj = Bus.objects.all()
            return render(request, "index.html", {'fname': fname, 'Bus':busobj})
        else:
            messages.error(request, "BAD CREDENTIALS")
            return redirect('/login')

    return render(request, 'login.html')

def signup_page(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please use some other username, thank you.")
            return redirect('/signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('/signup')

        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('/signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('/signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('/signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        

        # WELCOME EMAIL

        subject = "WELCOME TO PANDA"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to PANDA!! \n Thank you for visiting our website. \n We have also sent you a confirmation email, please confirm your email address inorder to activate you account. \n\n Thanking you, \n LARD, \n PANDA ADMINISTRATOR."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "PANDA ACCOUNT CONFIRMATION"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        messages.info(request, "ACCOUNT CREATED, TO LOGIN, PLEASE CHECK YOUR EMAIL TO ACTIVATE ACCOUNT.")
        return redirect('/login')


    return render(request, "signup.html")

def userview(request):
    context = {
        'user' : request.user,
    }
    return render(request, 'index.html', context)

def signout_page(request):
    logout(request)
    messages.success(request, "LOGGED OUT SUCCESSFULLY!")
    return redirect('/')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "ACCOUNT HAS BEEN SUCCESSFULLY ACTIVATED, PLEASE LOGIN, THANK YOU.")
        return render(request, 'login.html')
    else:
        messages.info(request, "ACTIVATION FAILED, PLEASE TRY AGAIN!")
        return redirect('/signup')


    return render(request, 'trinity_book.html')
    
def services_page(request):
    return render(request, 'services.html')

def contact_us_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        new_message = Contact(name = name, email = email, subject = subject, message = message)
        new_message.save()
        messages.success(request, "MESSAGE SENT, THANK YOU FOR CONTACTING PANDA")
      
    return render(request, 'contact_us.html')

def team_page(request):
    return render(request, 'team.html')

def bus_search(request):
    if request.method == "POST":
        source = request.POST['source']
        destination = request.POST['destination']
        date = request.POST['date']
        departure_time = request.POST['bustime']

        bussearchobj = Bus.objects.filter(source=source,destination=destination,date=date)
        return render(request, 'index.html', {'Bus':bussearchobj})
    else:
        busobj = Bus.objects.all()
        return render(request, 'index.html', {'Bus':busobj})
        
def bus_book(request, *args, **kwargs):
    if request.method == 'POST':
        busId=request.POST["bus_id"]
        bus_creation=BookBusForm()
        
        bus_name_id=Bus.objects.get(id=busId)
        bus_seats=bus_name_id.no_of_seats
        busSeats=int(bus_seats)
        new_dict={val:0 for val in range(busSeats)}

        #if Bus.objects.filter(id=busId).exists():
            #bus=Bus.objects.filter(id=busId).first()
            #temp =  bus.bookedseats.seats
            #seats=temp.split(',')
            #seats.pop()
            #i=0
            #for i in range(len(seats)):
                    #seat=seats[i]
                    #temp=int(seat)
                    #new_dict[temp]=1
            #return render(request, 'book_bus.html', {'bus':bus_creation, 'busId':busId, 'seats':new_dict})
        #else:
            #return render(request, 'book_bus.html', {'bus':bus_creation, 'busId':busId, 'seats':new_dict})
    
    return render(request, 'book_bus.html')