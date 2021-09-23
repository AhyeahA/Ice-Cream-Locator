from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=100)
    current_location_lat = models.FloatField()
    current_location_lng = models.FloatField()

    def __str__(self):
        return self.username

class IceCreamStore(models.Model):
    store_name = models.CharField(max_length=100)
    current_location_lat = models.FloatField()
    current_location_lon = models.FloatField()
    
    def __str__(self):
        return self.store_name
    

class IceCreamFlavors(models.Model):
    flavor_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9999, decimal_places=2)
    str_fk = models.ManyToManyField("IceCreamStore")

    def __str__(self):
        return self.flavor_name

class Favorite_Wantto_Visited_Store(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    store = models.ForeignKey(IceCreamStore,on_delete=models.CASCADE)
    favorite_store = models.BooleanField()
    want_to_visit = models.BooleanField()
    been_visited = models.BooleanField()


class FavoriteIceCreamFlavor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    flavor = models.ForeignKey(IceCreamFlavors, on_delete=models.CASCADE)



class RatingsAndReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    store = models.ForeignKey(IceCreamStore,on_delete=models.CASCADE) 
    rating = models.IntegerField(default = 1,validators=[MaxValueValidator(5), MinValueValidator(1)]) #constraint between 1 and 5
    reviews = models.TextField(max_length=1000)


    

class RecentSearch(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    search_content = models.TextField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add = True)





