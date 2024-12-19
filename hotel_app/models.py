from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid
# Custom User model to prevent conflicts with the default Django User model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid

# Custom User model to prevent conflicts with the default Django User model
class CustomUser(AbstractUser):
    is_public = models.BooleanField(default=False)  # To differentiate regular users
    customer_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Adding related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Custom related name to avoid conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Custom related name to avoid conflict
        blank=True,
    )

    def __str__(self):
        return self.username


    def save(self, *args, **kwargs):
        # Automatically generate customer_id based on the user's email address
        if not self.customer_id:
            # Generate a unique customer_id by combining the user's email (using a UUID if email is empty)
            self.customer_id = f"CID-{self.email.split('@')[0]}-{str(uuid.uuid4().int)[:6]}"
        super().save(*args, **kwargs)  # Call the save method of the parent class (AbstractUser)



from django.contrib.auth.hashers import make_password

class RoomBooking(models.Model):
    room = models.ForeignKey(
        'Room', to_field='room_no', on_delete=models.CASCADE, related_name="bookings"
    )  # Points to 'room_no' in the 'Room' table
    customer_id = models.CharField(max_length=255)  # VARCHAR field for customer ID
    First_name=models.CharField(max_length=255, blank=True, null=True) #added recently
    Lastname=models.CharField(max_length=255, blank=True, null=True)#added recently
    email_address=models.CharField(max_length=255, blank=True, null=True)#added recently
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    card_number = models.CharField(max_length=255, blank=True, null=True)  # Optional credit card field


    def __str__(self):
        return f"{self.customer_id} - {self.room.room_no}"

    def save(self, *args, **kwargs):
        if self._state.adding:  # Only hash credit card number when creating a new booking
            if self.card_number:
                self.card_number = make_password(self.card_number)  # Hashing the credit card number
        super().save(*args, **kwargs)



class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe'),
        ('presidential', 'Presidential Suite'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)  # Renamed for clarity
    features = models.TextField(help_text="Comma-separated list of features")
    # Image fields for specific room types
    image_living_room = models.ImageField(upload_to='room_images/', null=True, blank=True)
    image_bedroom = models.ImageField(upload_to='room_images/', null=True, blank=True)
    image_bathroom = models.ImageField(upload_to='room_images/', null=True, blank=True)
    # Room-specific details
    room_no = models.CharField(max_length=100, unique=True)  # Ensure room number is unique
    floor_no = models.IntegerField()  # Floor number
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES)  # Choices for room types
    is_occupied = models.BooleanField(default=False)  # Room occupation status
    current_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Current bill
    
    # Optional generic image (if you want one)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.room_no})"
    
    # Optionally, a method to calculate the total price for a stay
    def calculate_total_price(self, nights):
        return self.price * nights



class CustomerPayment(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to Django's User model
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Link to Room
    card_number = models.CharField(max_length=16)  # Card Number
    cvv = models.CharField(max_length=3)           # CVV
    expiry_date = models.DateField()              # Expiry Date
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} for {self.customer.username}"


    def __str__(self):
        return f"Payment {self.id} for {self.customer.username}"


# CheckIn model with a foreign key to the CustomUser model
class CheckIn(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=50)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Linking to CustomUser
    dob = models.DateField()
    purpose_of_stay = models.TextField()
    duration_of_stay = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    payment_status = models.CharField(
        max_length=50,
        choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Declined', 'Declined')],
    )

    def __str__(self):
        return f"CheckIn for {self.first_name} {self.last_name}"


from django.db import models
from .models import Room

class FoodOrder(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
