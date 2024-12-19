from django.contrib import admin
from .models import CustomUser, Room, CheckIn

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'capacity', 'room_status')  # Include room_status

    def room_status(self, obj):
        return "Occupied" if obj.is_occupied else "Available"

    room_status.short_description = "Room Status"  # Sets the column header in the admin panel
