from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from models import Room


def index(request):
    return render(request, "main.html")


class AddRoomView(View):
    def get(self, request):
        return render(request, "add_form.html")

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        name_exist = Room.objects.filter(name=name).exists()

        if not name:
            return HttpResponse("Name is required", status=400)

        if name_exist:
            return HttpResponse("Name already exist", status=400)

        if not capacity:
            return HttpResponse("Capacity is required", status=400)

        if capacity <= 0:
            return HttpResponse("Capacity must be positive number", status=400)

        new_room = Room(name=name, capacity=capacity, projector=projector)
        new_room.save()
        return HttpResponse("Room added", status=201)