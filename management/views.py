from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from management.models import Room, RoomReservation
from datetime import date, datetime


class ValidateMixin:
    def validate_data(self, request, room_id=None):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')

        if not name:
            return "Name is required"

        name_exist = Room.objects.filter(name=name).exclude(id=room_id).exists()
        if name_exist:
            return "Name already exist"

        try:
            capacity = int(capacity)
            if capacity <= 0:
                return "Capacity must be positive number"

        except ValueError:
            return "Capacity must be number"

        return None


def index(request):
    return render(request, "main.html")


class AddRoomView(ValidateMixin, View):
    def get(self, request):
        return render(request, "add_form.html")

    def post(self, request):
        error = self.validate_data(request)
        if error:
            return HttpResponse(error, status=400)

        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')

        new_room = Room(name=name, capacity=capacity, projector=projector)
        new_room.save()
        return HttpResponse("Room added<br><a href='/all-rooms/'>Rooms list</a>", status=201)


class RoomsView(View):
    def get(self, request):
        rooms = Room.objects.all()

        for room in rooms:
            reservations_dates = [reservations.date for reservations in room.roomreservation_set.all()]
            room.reserved = date.today() in reservations_dates

        if not rooms:
            return HttpResponse("No available rooms", status=400)

        ctx = {
            "rooms": rooms,
        }
        return render(request, "rooms_list.html", ctx)


class DeleteRoomView(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        room.delete()
        return redirect("/all-rooms/")


class EditRoomView(ValidateMixin, View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        ctx = {
            "room": room
        }
        return render(request, "edit_room_form.html", ctx)

    def post(self, request, room_id):
        error = self.validate_data(request, room_id)
        if error:
            return HttpResponse(error, status=400)

        room = Room.objects.get(id=room_id)
        room.name = request.POST.get('name')
        room.capacity = request.POST.get('capacity')
        room.projector = request.POST.get('projector')
        room.save()
        return redirect("/all-rooms/")


class RoomReservationView(View):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return HttpResponse("Room not found", status=404)
        room_reservations = RoomReservation.objects.filter(room=room).order_by('date')
        ctx = {
            "room": room,
            "room_reservations": room_reservations,
        }
        return render(request, "reserve_form.html", ctx)

    def post(self, request, room_id):
        res_date_str = request.POST.get('date')
        try:
            res_date = datetime.strptime(res_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return HttpResponse("Invalid date", status=400)

        if res_date < date.today():
            return HttpResponse("Date can't be from past", status=400)

        room = Room.objects.get(id=room_id)
        res_comment = request.POST.get('comment')
        reservation_exist = RoomReservation.objects.filter(room_id=room_id, date=res_date).exists()

        if reservation_exist:
            return HttpResponse("Room already reserved for that day", status=400)
        else:
            RoomReservation.objects.create(date=res_date, comment=res_comment, room=room)
            return redirect("/all-rooms/")


class RoomDetailsView(View):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return HttpResponse("Room not found", status=404)
        room_reservations = RoomReservation.objects.filter(room=room).order_by('date')
        ctx = {
            "room": room,
            "room_reservations": room_reservations,
        }
        return render(request, "room_details.html", ctx)


class SearchView(View):
    def get(self, request):
        searched_name = request.GET.get('search_name', '')
        searched_capacity = request.GET.get('search_capacity', 0)
        searched_projector = request.GET.get('search_projector', [0, 1])

        try:
            searched_rooms = Room.objects.filter(
                Q(name__icontains=searched_name) &
                Q(capacity__gte=searched_capacity) &
                Q(projector__in=searched_projector)
            )
        except Room.DoesNotExist:
            searched_rooms = []

        return render(request, "searched_rooms.html", {"searched_rooms": searched_rooms})
