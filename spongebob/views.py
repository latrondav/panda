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
from django.utils.encoding import force_bytes, force_text
from . token import generate_token
from django.core.mail import EmailMessage, send_mail

# Create your views here.
#def home(request):
    #return HttpResponse("Hello World")

def home_page(request):
    return render(request, 'index.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "welcome.html", {'fname': fname})
        else:
            messages.error(request, "BAD CREDENTIALS")
            return redirect('/')

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
            return redirect('sign up/')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('sign up/')

        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('sign up/')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('sign up/')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('sign up/')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_Name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request, "YOUR ACCOUNT HAS BEEN SUCCESSFULLY CREATED. \n WE HAVE SENT YOU A CONFIRMATION EMAIL, PLEASE CONFIRM YOUR EMAIL IN ORDER TO ACTIVATE ACCOUNT.")

        # WELCOME EMAIL

        subject = "Welcome to PANDA - Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to PANDA!! \n Thank you for visiting our website. \n We have also sent you a confirmation email, please confirm your email address inorder to activate you account. \n\n Thanking you, \n LARD, \n PANDA ADMINISTRATOR."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email @PANDA - Django Login!"
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
        return redirect('login/')


    return render(request, "signup.html")

def signout_page(request):
    logout(request)
    messages.success(request, "LOGGED OUT SUCCESSFULLY!")
    return redirect('index/')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
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
        return render(request, 'activation_failed.html')

def trinity_home_page(request):
    return render(request, 'trinity_home.html')

def trinity_book_page(request):
    return render(request, 'trinity_book.html')