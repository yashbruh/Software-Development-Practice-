from django.http import HttpResponseRedirect,HttpResponseNotFound, HttpResponseBadRequest
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate, login
from .models import CustomUser  # Use CustomUser if you're using a custom user model
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from .models import Room, RoomBooking
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from decimal import Decimal
from .models import Room, RoomBooking, FoodOrder
import json
import random
from django.core.exceptions import ValidationError
from datetime import date, datetime
import string


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the user exists
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'Email not registered'})

        # Generate a 6-digit random code
        code = get_random_string(6, '0123456789')

        # Send the code to the user's email
        send_mail(
            'Your Password Reset Code',
            f'Your password reset code is {code}',
            settings.DEFAULT_FROM_EMAIL,  # Ensure this is set correctly in settings.py
            [email],
            fail_silently=False,
        )

        # Store the code in session
        request.session['reset_code'] = code
        request.session['email'] = email

        return redirect('verify_code')  # Redirect to code verification page

    return render(request, 'forgot_password.html')

# View to handle verification of the code
def verify_code_view(request):
    if request.method == 'POST':
        code_entered = request.POST.get('code')
        code_sent = request.session.get('reset_code')

        if code_entered == code_sent:
            return redirect('reset_password')  # Redirect to reset password page
        else:
            return render(request, 'verify_code.html', {'error': 'Invalid code'})

    return render(request, 'verify_code.html')


# View to handle resetting the password
def reset_password_view(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        email = request.session.get('email')

        # Hash the new password
        hashed_password = make_password(new_password)

        # Update the user's password
        user = CustomUser.objects.get(email=email)
        user.password = hashed_password
        user.save()

        # Clear session data after password change
        del request.session['reset_code']
        del request.session['email']

        return redirect('login')  # Redirect to login page after password reset

    return render(request, 'reset_password.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # First, attempt to authenticate using the `auth_user` model
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            # If not found in `auth_user`, attempt to authenticate using the `hotel_app_customuser` model
            from hotel_app.models import CustomUser  # Import your custom user model
            user = CustomUser.objects.filter(email=email).first()  # Adjust the field accordingly
            
            if user is not None and user.check_password(password):
                print(f"User: {user}, Username: {user.username}")

                print(f"User authenticated successfully: {user.username}")  # Debug: print user after successful authentication
                login(request, user)
                if user.is_staff:  # If the user is an admin
                    return redirect('admin_homepage')
                return redirect('public_homepage')  # Redirect to public homepage

        if user is not None:
            print(f"User: {user}, Username: {user.username}")

            print(f"User authenticated successfully: {user.username}")  # Debug: print user after successful authentication
            login(request, user)
            if user.is_staff:  # If the user is an admin
                return redirect('admin_homepage')
            return redirect('public_homepage')  # Redirect to public homepage
        else:
            print("email and password ", email, password)
            print("Authentication failed")  # Debug: print error when authentication fails
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Room  # Adjust the import to your project structure

def update_room_occupancy(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')  # Get room_number from the POST request
        if not room_number:
            return JsonResponse({'error': 'Room number is required.'})

        try:
            # Fetch the room using the room number
            room = get_object_or_404(Room, room_no=room_number)

            # Check if `is_occupied` is already 0
            if room.is_occupied == 0:
                return JsonResponse({'success': 'Room is already unoccupied.'})
            
            # Update the room's occupancy
            room.is_occupied = 0
            room.save()

            return JsonResponse({'success': f'Room {room_number} occupancy updated successfully.'})
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'})

    return JsonResponse({'error': 'Invalid request method. Use POST.'})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')

        # Check if username is already taken
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'register.html')

        # Check if email is already taken
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use!")
            return render(request, 'register.html')

        try:
            # Create the user
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f"User {user.username} created successfully!")

            # Automatically log in the user after registration
            login(request, user)
            return redirect('public_homepage')
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return render(request, 'register.html')

    return render(request, 'register.html')



def public_homepage(request):
    # Get the current date
    current_date = timezone.now().date()

    # Fetch filter inputs
    check_in_date = request.GET.get('check_in_date', None)
    check_out_date = request.GET.get('check_out_date', None)
    room_type = request.GET.get('room_type', None)
    price_min = request.GET.get('price_min', None)
    price_max = request.GET.get('price_max', None)

    # Query to fetch all available rooms
    rooms = Room.objects.all()

    # Apply filters dynamically
    if check_in_date and check_out_date:
        check_in_date = timezone.datetime.strptime(check_in_date, "%Y-%m-%d").date()
        check_out_date = timezone.datetime.strptime(check_out_date, "%Y-%m-%d").date()

        # Exclude rooms with bookings that overlap the specified dates
        rooms = rooms.exclude(
            roombooking__check_in_date__lt=check_out_date,
            roombooking__check_out_date__gt=check_in_date,
        ).distinct()

    if room_type:
        rooms = rooms.filter(room_type__iexact=room_type)

    if price_min:
        rooms = rooms.filter(price__gte=price_min)

    if price_max:
        rooms = rooms.filter(price__lte=price_max)

    # Pass filtered rooms to template
    context = {
        'rooms': rooms,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        'room_type': room_type,
        'price_min': price_min,
        'price_max': price_max,
    }
    return render(request, 'public_homepage.html', context)


# parking #
def generate_parking_spot():
    
    # Generate a random parking spot like A9, B5, etc.
    letter = random.choice(string.ascii_uppercase)  # Random uppercase letter
    number = random.randint(1, 99)  # Random number between 1 and 99
    return f"{letter}{number}"


# room #

def room_details(request, room_id):
    # Fetch the room object using its ID
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email_address = request.POST.get("email")
        card_number = request.POST.get("credit_card_number")  # Ensure retrieval
        check_in_date = request.POST.get("check_in_date")
        check_out_date = request.POST.get("check_out_date")
        parking_needed = request.POST.get("parking_needed")  # Checkbox value

        # Hash the card number if provided
        if card_number:
            card_number = make_password(card_number)

        # Validate and parse dates
        try:
            check_in = timezone.datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out = timezone.datetime.strptime(check_out_date, "%Y-%m-%d")
            room.is_occupied = 1
            room.current_bill=room.price
            room.save()

            if check_out <= check_in:
                messages.error(request, "Check-out date must be after check-in date.")
                return redirect("room_details", room_id=room_id)
            total_price = room.price * (check_out - check_in).days
        except ValueError:
            messages.error(request, "Invalid dates provided.")
            return redirect("room_details", room_id=room_id)

        # Generate parking spot if requested
        parking_spot = None
        if parking_needed:
            parking_spot = generate_parking_spot()

        # Fetch the customer_id from CustomUser table based on email
        try:
            customer = CustomUser.objects.get(email=email_address)
            custom_customer_id = customer.customer_id
        except CustomUser.DoesNotExist:
            messages.error(request, "No customer found with the provided email.")
            return redirect("room_details", room_id=room_id)

        # Save the booking
        RoomBooking.objects.create(
            room=room,
            customer_id=custom_customer_id,
            First_name=first_name,
            Lastname=last_name,
            email_address=email_address,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            card_number=card_number,
        )

        # Pass all details to the success page
        return render(request, "booking_success.html", {
            "first_name": first_name,
            "last_name": last_name,
            "room_id": room.id,
            "room_name": room.name,
            "total_price": total_price,
            "parking_spot": parking_spot,  # Parking spot to be shown
        })

    return render(request, "room_details.html", {"room": room})


# Admin homepage view
def admin_homepage(request):
    rooms = Room.objects.all()
    return render(request, 'admin_homepage.html', {'rooms': rooms})


# food order
def place_order(request):
    if request.method == 'POST':
        room_no = request.POST.get('room_no')
        selected_dishes = request.POST.getlist('dishes[]')

        # Input validation
        if not room_no or not selected_dishes:
            return JsonResponse({'error': 'Room number and dishes are required!'}, status=400)

        try:
            # Validate room existence
            room = Room.objects.get(room_no=room_no)

            # Calculate total dish price
            try:
                dish_total = sum(Decimal(dish_price) for dish_price in selected_dishes)
            except:
                return JsonResponse({'error': 'Invalid dish price format!'}, status=400)

            # Update the room's current bill
            room.current_bill += dish_total
            room.save()

            # Return success message
            return JsonResponse({'success': 'Order placed successfully!', 'new_bill': float(room.current_bill)})

        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room not found!'}, status=404)

    return JsonResponse({'error': 'Invalid request method!'}, status=405)




def checkin_page(request):
    rooms = Room.objects.filter(is_occupied=False)
    today = date.today().strftime('%Y-%m-%d')
    return render(request, 'checkin.html', {'rooms': rooms, 'today': today})



def checkin(request):
    if request.method == 'POST':
        try:
            room_no = request.POST.get('room_no')
            first_name = request.POST.get('First_name')
            last_name = request.POST.get('Lastname')
            email = request.POST.get('email_address')
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')
            card_number = request.POST.get('card_number')  # Optional
            customer_id = 'admin_id001'  # Fixed value as per your requirement

            # Validate dates
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()

            if check_in_date < date.today():
                raise ValidationError("Check-in date cannot be in the past.")

            if check_out_date <= check_in_date:
                raise ValidationError("Check-out date must be after check-in date.")

            # Get the room instance by room_no
            room = get_object_or_404(Room, room_no=room_no)

            # Calculate total price based on the number of nights
            nights = (check_out_date - check_in_date).days
            total_price = room.price * nights

            # Create the booking
            booking = RoomBooking.objects.create(
                room=room,
                customer_id=customer_id,
                First_name=first_name,
                Lastname=last_name,
                email_address=email,
                check_in=check_in_date,
                check_out=check_out_date,
                card_number=card_number,
                total_price=total_price,
            )

            # Mark the room as occupied
            room.is_occupied = True
            room.save()

            # Optional: Send a confirmation email
            send_mail(
                subject="Booking Confirmation",
                message=(f"Dear {first_name},\n\n"
                         f"Your booking for Room {room_no} has been confirmed.\n"
                         f"Check-in: {check_in_date}\n"
                         f"Check-out: {check_out_date}\n"
                         f"Total Price: ${total_price}\n\n"
                         f"Thank you for choosing our service!"),
                from_email="hotelsrh3.com",
                recipient_list=[email],
                fail_silently=True,
            )

            # Redirect to booking success page with the booking ID
            return redirect('booking_success', booking_id=booking.id)

        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred.'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)



def reset_room_status(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        if not room_number:
            return HttpResponseBadRequest("Room number is required.")

        # Fetch the room object and reset its status
        room = get_object_or_404(Room, room_no=room_number)
        room.is_occupied = False
        room.current_bill = 0  # Reset the bill
        room.save()

        # Redirect to the admin homepage or any other page
        return redirect('admin_homepage')  # Update with your desired redirection page

    return HttpResponseBadRequest("Invalid request method.")


def checkout_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room = get_object_or_404(Room, room_no=room_number)

        if room.is_occupied:
            # Redirect to view_bill with the room number as a query parameter
            return HttpResponseRedirect(reverse('view_bill') + f"?room_no={room_number}")

    return HttpResponseRedirect(reverse('admin_homepage'))



def view_bill(request):
    # Get the room number from the query parameters
    room_number = request.GET.get('room_no')
    if room_number:
        try:
            # Fetch the room by room number
            room = Room.objects.get(room_no=room_number)
            
            # Fetch the latest booking for the given room number
            latest_booking = RoomBooking.objects.filter(room=room).order_by('-id').first()
            
            if not latest_booking:
                return HttpResponseNotFound("No booking found for this room.")

            # Extract the required details
            first_name = latest_booking.First_name
            last_name = latest_booking.Lastname
            latest_bill = room.current_bill
            room_type = room.room_type

            # Render the bill information on the page
            context = {
                'room_number': room_number,
                'first_name': first_name,
                'last_name': last_name,
                'latest_bill': latest_bill,
                'room_type': room_type,
            }
            return render(request, 'view_bill.html', context)

        except Room.DoesNotExist:
            return HttpResponseNotFound("No room matches the given query.")
    else:
        return HttpResponseBadRequest("Room number is required.")

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import RoomBooking

def fetch_details(request):
    if request.method == 'GET':
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')    
        
        # Retrieve the details from RoomBooking based on first_name and last_name
        booking = RoomBooking.objects.filter(First_name=first_name, Lastname=last_name).last()

        if booking:
            data = {
                'room_no': booking.room.room_no,
                'email_address': booking.email_address,
                'check_in_date': booking.check_in.strftime('%Y-%m-%d'),
                'check_out_date': booking.check_out.strftime('%Y-%m-%d'),
                'card_number': booking.card_number
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'No booking found'}, status=404)



# Booking success view
def booking_success(request, booking_id=None):
    if booking_id:
        booking = get_object_or_404(RoomBooking, id=booking_id)

        first_name = booking.First_name
        last_name = booking.Lastname
        room_no = booking.room.room_no
        room_type = booking.room.room_type
        total_price = booking.total_price
        parking_spot = booking.room.parking_spot if hasattr(booking.room, 'parking_spot') else "Unknown"
    else:
        first_name, last_name, room_no, room_type, total_price, parking_spot = ("Unknown",) * 6

    return render(request, "booking_success.html", {
        "room_name": room_type,
        "total_price": total_price,
        "first_name": first_name,
        "last_name": last_name,
        "room_id": room_no,
        "message": "Your booking was successful!",
    })


