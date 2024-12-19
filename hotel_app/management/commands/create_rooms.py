from django.core.management.base import BaseCommand
from hotel_app.models import Room

class Command(BaseCommand):
    help = "Create default room objects"

    def handle(self, *args, **kwargs):
        # Creating default rooms with all required fields
        Room.objects.create(
            name="King Size Room",
            description="Spacious room with a king-sized bed and modern amenities.",
            price=120.00,
            capacity=2,
            room_status=True,
            features="Free Wi-Fi, Air Conditioning, Mini Bar",
            image_living_room="/static/images/room_images/.livingroom1.png",
            image_bedroom="/static/images/room_images/kingsize_bed.png",
            image_bathroom="/static/images/room_images/bathroom1.png",
            room_no="101",  # Room number
            floor_no=1,  # Floor number
            room_type="Suite",  # Room type
            is_occupied=False,  # Room is not occupied initially
            current_bill=0,  # No bill initially
            image="/static/images/room_images/kingsize_room.png",  # Optional image
        )
        Room.objects.create(
            name="Villa",
            description="Spacious room with a spacious hall, bathroom, balcony and modern amenities.",
            price=559.00,
            capacity=6,
            room_status=True,
            features="Free Wi-Fi, Air Conditioning, Mini Bar, pool, spa, balcony with garden",
            image_living_room="/static/images/room_images/villa_livingroom.jpg",
            image_bedroom="/static/images/room_images/villa_bedroom.jpg",
            image_bathroom="/static/images/room_images/villa_bathroom.jpg",
            room_no="102",
            floor_no=2,
            room_type="Villa",
            is_occupied=False,
            current_bill=0,
            image="/static/images/room_images/villa.png",
        )
        Room.objects.create(
            name="Suite",
            description="Spacious room with a spacious hall, bathroom, conference break room and modern amenities.",
            price=399.00,
            capacity=6,
            room_status=True,
            features="Free Wi-Fi, Air Conditioning, Mini Bar, pool, balcony",
            image_living_room="/static/images/room_images/living_room1.png",
            image_bedroom="/static/images/room_images/suite_bedroom.jpg",
            image_bathroom="/static/images/room_images/suite_bathroom.jpg",
            room_no="103",
            floor_no=3,
            room_type="Suite",
            is_occupied=False,
            current_bill=0,
            image="/static/images/room_images/suite.png",
        )
        Room.objects.create(
            name="Queen Size Room",
            description="Comfortable room with a queen-sized bed.",
            price=100.00,
            capacity=2,
            room_status=True,
            features="Free Wi-Fi, Air Conditioning",
            image_living_room="/static/images/room_images/.livingroom1.png",
            image_bedroom="/static/images/room_images/queensize_bed1.jpg",
            image_bathroom="/static/images/room_images/bathroom2.png",
            room_no="104",
            floor_no=1,
            room_type="Standard",
            is_occupied=False,
            current_bill=0,
            image="/static/images/room_images/queensize_room.png",
        )
        
        self.stdout.write("Rooms created successfully!")




