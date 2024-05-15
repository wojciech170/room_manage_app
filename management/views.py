from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from management.models import Room


class ValidateMixin:
    def validate_data(self,request, room_id=None):
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
        return HttpResponse("Room added", status=201)


class RoomsView(View):
    def get(self, request):
        rooms = Room.objects.all()
        if not rooms:
            return HttpResponse("No available rooms", status=400)
        ctx = {
            "rooms": rooms
        }
        return render(request, "rooms_list.html", ctx)


class DeleteRoomView(View):
    def get(self, request):
        id = request.GET.get('id')
        room = Room.objects.get(id=id)
        room.delete()
        return redirect("all-rooms/")


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

