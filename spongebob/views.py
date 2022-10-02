from cgi import print_exception
from datetime import date
import email
from email import message
import imp
from multiprocessing import context
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
from . models import Contact, Bus, BookedSeats, BusBooking
from . token import generate_token
from .forms import BookBusForm
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
            return render(request, "index.html", {'fname': fname})
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
        myuser.first_name = fname.upper()
        myuser.last_name = lname.upper()
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
    
def find_bus_page(request):
    busobj = Bus.objects.all()

    context={
        'Bus':busobj
    }
    return render(request, 'find_bus.html', context)

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

def bus_search_page(request):
    if request.method == "POST":
        source = request.POST['source']
        destination = request.POST['destination']
        date = request.POST['date']

        bussearchobj = Bus.objects.filter(source=source,destination=destination,date=date)
        if bussearchobj:
            context={
                'Bus':bussearchobj
            }
            return render(request, 'find_bus.html', context)
        else:
            context={
                'error':f"No buses available for that route and date."
            }
            return render(request, 'find_bus.html', context)
    else:
        return render(request, 'find_bus.html')
        
def bus_book_page(request, *args, **kwargs):
    if request.method == 'POST':
        busId=request.POST['busId']
        unit_price=request.POST['unit_price']
        bus_creation=BookBusForm()
        
        bus_name_id=Bus.objects.get(id=busId)
        bus_seats=bus_name_id.no_of_seats
        busSeats=int(bus_seats)
        new_dict= {val:0 for val in range(busSeats)}

        if Bus.objects.filter(id=busId).exists():
            bus= Bus.objects.filter(id=busId).first()
            temp = bus.bookedseats.seats
            seats=temp.split(',')
            seats.pop()
            i=0
            for i in range(len(seats)):
                    seat=seats[i]
                    temp=int(seat)
                    new_dict[temp]=1

            context ={'bus':bus_creation, 'busId':busId, 'seats':new_dict, 'unit_price':unit_price}

            return render(request, 'book_bus.html', context)
        else:
            return render(request, 'book_bus.html', context)

    return render(request, 'book_bus.html')
    

def booking_details_page(request, *args, **kwargs):
    if request.method == 'POST':
        bus_id=request.POST.get('busId')
        seat_nos=request.POST.get('seat_nos')
        seat_nos=seat_nos[:-1]
        no_of_seats=int(request.POST.get('count'))
        unit_price=request.POST.get('unit_price')
        total_price=request.POST.get('total_price')
        payment_method=request.POST.get('payment_method')
        phone_no=request.POST.get('phone_no')
        bus_station=request.POST.get('bus_station')
        
        bus=Bus.objects.get(id=bus_id)
        if bus:
            if bus.remaining_seats > no_of_seats or bus.remaining_seats == int(no_of_seats) :
                username=request.user.username
                user_id=request.user.id
                email=request.user.email
                bus_admin_id=bus.bus_admin_id
                number_plate=bus.number_plate
                name=bus.name
                source=bus.source
                destination=bus.destination
                date=bus.date
                seats= seat_nos
                time=bus.departure_time
                bus_remaining_seats=bus.remaining_seats - int(no_of_seats)
               
                booked_seats=bus.bookedseats.seats
                booked_seats += ',' + seats
                #BookedSeats.objects.update(seats=booked_seats, bus=bus)
                BookedSeats.objects.filter(bus_id=bus).update(seats=booked_seats)



                #try:
                    #booked_seats, created=BookedSeats.objects.get_or_create(id=bus_id)
                    
                    #if created:
                        #booked_seats.seats += seats
                        #booked_seats.save()
                        #print(booked_seats)
                #except:
                        #bus=Bus.objects.filter(id=bus_id).first()
                        #booked_seats=BookedSeats(seats=seat_nos, bus=bus)
                        #booked_seats.save()
                
             
                Bus.objects.filter(id=bus_id).update(remaining_seats=bus_remaining_seats)
                booking_details=BusBooking.objects.create(
                    bus_admin_id=bus_admin_id,
                    user_name=username,
                    user_email=email,
                    user_id=user_id,
                    number_plate=number_plate,
                    source=source,
                    destination=destination,
                    bus_name=name,
                    date=date,
                    unit_price=unit_price,
                    total_price=total_price,
                    payment_method=payment_method,
                    bus_id=bus_id,
                    time=time,
                    no_of_seats=no_of_seats,
                    seat_numbers=seat_nos,
                    phone_no=phone_no,
                    bus_station=bus_station,
                )
                context={
                    'booking_details':booking_details,
                    'seat_price':unit_price,
                    'bus':bus
                }
                print('============Booking ID==========', booking_details.id)     
                return render(request,'booking_details.html',locals())
            else:
                context={
                    'error':f'Input {bus.remaining_seats} seat/s or less.'
                }    
                return render(request,'booking_details.html', context)
        else:
            context={
              'error':'Please input a valid Bus ID'
            }    
            return render(request,'booking_details.html', context)        
    else:
        return render(request,'booking_details.html')

    #return render(request,'booking_details.html')    

def bookings_page(request):
    userId = request.user.id
    bookings = BusBooking.objects.filter(user_id=userId)
    if bookings:
        context={
            'bookings':bookings
        }
        return render(request, 'bookings.html', context)
    else:
        context={
            'error':f'You have no bookings yet please find and book a bus, thank you.'
        }
        return render(request, 'bookings.html', context)

    #return render(request, 'bookings.html')

def booked_page(request):
    booked_id = request.POST['booked_id']
    booked = BusBooking.objects.get(id=booked_id)
    if booked:
        context={
            'booked':booked
        }
        return render(request, 'booked.html', context)
    else:
        return render(request, 'booked.html')

def buses_page(request):
    busobj = Bus.objects.all()

    context={
        'Bus':busobj
    }
    return render(request, 'buses.html', context)

def add_bus_page(request):
    if request.method == 'POST':
        bus_admin_id=request.user.id
        name = request.POST['name']
        image = request.FILES['image']
        number_plate = request.POST['number_plate']
        source = request.POST['source']
        destination = request.POST['destination']
        no_of_seats = request.POST['no_of_seats']
        remaining_seats = request.POST['remaining_seats']
        price = request.POST['price']
        date = request.POST['date']
        departure_time = request.POST['departure_time']

        bus = Bus(bus_admin_id = bus_admin_id, name = name, image = image, number_plate = number_plate, source = source, destination = destination, no_of_seats = no_of_seats, remaining_seats = remaining_seats, price = price, date = date, departure_time = departure_time)
        bus.save()
        messages.success(request, "BUS ADDITION SUCCESSFUL, THANK YOU FOR USING PANDA")
        return render(request, 'fleet.html')
    else:
        return render(request, 'fleet.html')

def update_fleet_page(request):
    if request.method == 'POST':
        bus_id=request.POST['busId']
        source = request.POST['source']
        destination = request.POST['destination']
        remaining_seats = request.POST['remaining_seats']
        date = request.POST['date']
        departure_time = request.POST['departure_time']

        Bus.objects.filter(id=bus_id).update(source=source, destination=destination, remaining_seats=remaining_seats, date=date, departure_time=departure_time)
        messages.success(request, "FLEET UPDATED SUCCESSFUL, RETURN TO HOMEPAGE AND THANK YOU FOR USING PANDA")
        return render (request, 'fleet.html')
    else:
        return render (request, 'fleet.html')

    #return render(request, 'fleet.html')

def fleets_page(request):
    bus_admin_id = request.user.id

    fleets = Bus.objects.filter(bus_admin_id = bus_admin_id)
    if fleets:
        context={
            'fleets':fleets
        }
        return render(request, 'fleet.html', context)
    else:
        return render(request, 'fleet.html')

    #return render(request, 'add_bus.html')

def fleets_reports_page(request):
    bus_admin_id = request.user.id

    bus_details = BusBooking.objects.filter(bus_admin_id = bus_admin_id)
    if bus_details:
        context={
            'bus_details':bus_details,
        }
        return render(request, 'fleets_reports.html', context)
    else:
        return render(request, 'fleets_reports.html')