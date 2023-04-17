
Тестовое задание в компанию

Не разделяла по view, repository и тд, потому что хотела оставить только то, что нужно для решения тестового
Дословное описание задачи:

class Hotel(models.Model):
    title = models.CharField(max_length=128)
    likes = models.PositiveIntegerField()
    dislikes = models.PositiveIntegerField()
    
    
class Room(models.Model):
    title = models.CharField(max_length=128)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,
    related_name='rooms')
    
    
class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
    related_name='reservations')
    start = models.DateField()
    end = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    related_name='reservations')
    
1) Get the list of users are living in hotel Maryland
2) What should be fixed and improved in these views (in terms of
concurrency)

def like_hotel_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.likes += 1
    hotel.save()
    return HttpResponse({'details': 'success'})
    
    
def dislike_holet_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.dislikes += 1
    hotel.save()
    return HttpResponse({'details': 'success'})
    
3) Get list of all rooms with sold_out(True|False) sign (attribute of room
object). Sold_out sign should be calculated for user’s move in and move out
dates.
def get_rooms_list_with_sold_out_sign(move_in, move_out):
pass

4) Get list of hotels with only one free room (for today)
