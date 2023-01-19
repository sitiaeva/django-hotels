from .models import Hotel, Room, User

from datetime import date
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count, FilteredRelation, Case, Value, When, F
from django.shortcuts import get_object_or_404
from django.db import transaction


def index(request):
    return HttpResponse("Hello, world. HOTELS")


def users_in_hotel_view(request):
    """Get the list of users are living in hotel Maryland"""
    q = User.objects.filter(Q(reservations__start__lte=date.today())
                            & Q(reservations__end__gte=date.today())
                            & Q(reservations__room__hotel__title="Maryland"))

    return JsonResponse(list(q.values()), safe=False)


def like_hotel_view(request):
    with transaction.atomic():
        hotel_id = 3
        hotel = get_object_or_404(Hotel.objects.select_for_update(), id=hotel_id)
        hotel.likes += 1
        hotel.save()
        return HttpResponse({'details': 'success'})


def dislike_holet_view(request):
    hotel_id = 3
    with transaction.atomic():
        hotel = get_object_or_404(Hotel.objects.select_for_update(), id=hotel_id)
        hotel.dislikes += 1
        hotel.save()
        return HttpResponse({'details': 'success'})


def rooms_list_with_sold_out_sign_view(request):
    """Get list of all rooms with sold_out(True|False) sign (attribute of room
            object). Sold_out sign should be calculated for user’s move in and move out
            dates."""

    filter_for_reservations = FilteredRelation('reservations', condition=~Q(
        Q(reservations__end__lt=date.today())
        | Q(reservations__start__gt=date.today())))

    case_for_sold_out = Case(When(filtered_reservations__isnull=True, then=Value('False')), default=Value('True'))

    q = Room.objects \
        .annotate(filtered_reservations=filter_for_reservations) \
        .annotate(sold_out=case_for_sold_out)
    return JsonResponse(list(q.values()), safe=False)


def hotels_with_one_free_room_view(request):
    """Get list of hotels with only one free room (for today)"""
    filter_for_reservations = Q(rooms__reservations__start__lte=date.today()) \
                              & Q(rooms__reservations__end__gte=date.today())

    filtered_reservations = Count('rooms__reservations',
                                  filter=filter_for_reservations,
                                  distinct=True)
    rooms_count = Count('rooms', distinct=True)

    q = Hotel.objects \
        .annotate(rooms_count=rooms_count) \
        .annotate(filtered_reservations=filtered_reservations) \
        .annotate(free_rooms_num=F('rooms_count') - F('filtered_reservations'))\
        .filter(free_rooms_num=1)
    return JsonResponse(list(q.values()), safe=False)
