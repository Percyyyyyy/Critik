import json
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import localtime

class TypeResto(models.Model):
    noType = models.AutoField(primary_key=True)
    nomType = models.CharField(max_length=20)

    def __str__(self):
        return self.nomType

class Restaurant(models.Model):
    noRestaurant = models.AutoField(primary_key=True)
    nomRestaurant = models.CharField(max_length=255) 
    villeRestaurant = models.CharField(max_length=25)
    imageRestaurant = models.URLField(default='https://example.com/default_image.jpg')
    typeRestaurant = models.ForeignKey(TypeResto, on_delete=models.DO_NOTHING)
    noteRestaurant = models.FloatField(null=True)
    adresseRestaurant = models.CharField(max_length=100, default="Inconnue")
    def __str__(self):
        return self.nomRestaurant

def update_note_restaurant(instance):
    avg_note = instance.commentaire_set.aggregate(avg_note=Avg('note'))['avg_note']
    avg_note_rounded = round(avg_note, 1) if avg_note is not None else 0
    instance.noteRestaurant = avg_note_rounded
    instance.save()

class Commentaire(models.Model):
    noCommentaire = models.AutoField(primary_key=True)
    noRestaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    userName = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    commentaire = models.TextField()
    note = models.IntegerField(default=0)
    dateCommentaire = models.DateField(auto_now_add=True)
    old_data = models.JSONField(null=True, blank=True) 

    def __str__(self):
        return f"{self.userName.username} - {self.noRestaurant.nomRestaurant} ({self.note})"

@receiver(post_save, sender=Commentaire)
def update_note_restaurant_on_commentaire_save(sender, instance, **kwargs):
    update_note_restaurant(instance.noRestaurant)

@receiver(post_delete, sender=Commentaire)
def update_note_restaurant_on_commentaire_delete(sender, instance, **kwargs):
    update_note_restaurant(instance.noRestaurant)
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    old_data = models.TextField(null=True, blank=True)
    new_data = models.TextField(null=True, blank=True)

    def __str__(self):
        local_timestamp = localtime(self.timestamp)
        formatted_time = local_timestamp.strftime("%d/%m/%Y %Hh%Mm%Ss")
        return f"{self.action} - {formatted_time}"

    def get_differences(self):
        old_data_dict = json.loads(self.old_data) if self.old_data else {}
        new_data_dict = json.loads(self.new_data) if self.new_data else {}

        differences = []
        for key, old_value in old_data_dict.items():
            new_value = new_data_dict.get(key)
            if old_value != new_value:
                differences.append(f"{key}: {old_value} -> {new_value}")

        return differences