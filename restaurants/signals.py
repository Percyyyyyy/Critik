from datetime import date, datetime
import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from restaurants.middleware import get_current_user
from restaurants.models import Restaurant, Commentaire, Log
from django.db.models.signals import pre_save
from django.utils.dateformat import DateFormat


@receiver(post_save, sender=Restaurant)
def log_new_restaurant(sender, instance, created, **kwargs):
    if created:
        Log.objects.create(
            user=instance.user,
            action=f"Restaurant {instance.nomRestaurant} situé à {instance.villeRestaurant} ajouté"
        )
        
@receiver(post_save, sender=Restaurant)
def log_modified_restaurant(sender, instance, created, **kwargs):
    print(f"[DEBUG - post_save Restaurant] Début log modif restaurant ID {instance.pk}")

    if created:
        print(f"[DEBUG - post_save Restaurant] Nouveau restaurant ajouté: {instance.nomRestaurant}")
        return

    if hasattr(instance, 'old_data') and instance.old_data:
        print(f"[DEBUG - post_save Restaurant] Diff détectée sur restaurant ID {instance.pk}")
        print(f"[DEBUG - post_save Restaurant] old_data: {instance.old_data}")
        print(f"[DEBUG - post_save Restaurant] new_data: {instance.new_data}")

        old_data_json = json.dumps(instance.old_data, indent=4)
        new_data_json = json.dumps(instance.new_data, indent=4)

        Log.objects.create(
            action=f"Modification du {instance.typeRestaurant} {instance.nomRestaurant} situé à  {instance.villeRestaurant}",
            user=getattr(instance, 'user', get_current_user()),
            old_data=old_data_json,
            new_data=new_data_json,
        )
        print(f"[DEBUG - post_save Restaurant] Log créé pour restaurant ID {instance.pk}")
    else:
        print(f"[DEBUG - post_save Restaurant] Aucune modification à logger pour restaurant ID {instance.pk}")

    print(f"[DEBUG - post_save Restaurant] Fin log modif restaurant ID {instance.pk}")

@receiver(post_save, sender=Commentaire)
def log_new_commentaire(sender, instance, created, **kwargs):
    if created:
        Log.objects.create(
            user=instance.userName,
            action=f"Commentaire ajouté au restaurant '{instance.noRestaurant.nomRestaurant}': {instance.commentaire[:50]}..."
        )
        
@receiver(post_save, sender=Commentaire)
def log_modified_commentaire(sender, instance, created, **kwargs):
    print(f"[DEBUG - post_save] Début log modif commentaire ID {instance.noCommentaire}")

    if not created and hasattr(instance, 'old_data') and instance.old_data:
        print(f"[DEBUG - post_save] Diff détectée sur commentaire ID {instance.noCommentaire}")
        print(f"[DEBUG - post_save] old_data: {instance.old_data}")
        print(f"[DEBUG - post_save] new_data: {instance.new_data}")

        Log.objects.create(
            user=instance.userName,
            action=f"Modification du commentaire du restaurant {instance.noRestaurant.nomRestaurant}",
            old_data=json.dumps(instance.old_data),
            new_data=json.dumps(instance.new_data),
        )
        print(f"[DEBUG - post_save] Log créé pour commentaire ID {instance.noCommentaire}")
    else:
        print(f"[DEBUG - post_save] Aucune modification à logger pour commentaire ID {instance.noCommentaire}")

    print(f"[DEBUG - post_save] Fin log modif commentaire ID {instance.noCommentaire}")

@receiver(post_delete, sender=Restaurant)
def log_deleted_restaurant(sender, instance, **kwargs):
    user = get_current_user()
    if user:
        if user.is_superuser:
            Log.objects.create(
                user=user,
                action=f"[ADMIN] {user.username} a supprimé le restaurant \"{instance.nomRestaurant}\" situé à \"{instance.villeRestaurant}\""
            )
        else:
            Log.objects.create(
                user=user,
                action=f"{user.username} a supprimé le restaurant \"{instance.nomRestaurant}\" situé à \"{instance.villeRestaurant}\""
            )
@receiver(post_delete, sender=Commentaire)
def log_deleted_commentaire(sender, instance, **kwargs):
    user = get_current_user()
    if user:
        if user.is_superuser:
            Log.objects.create(
                user=user,
                action=f"[ADMIN] {user.username} a supprimé ce commentaire: \"{instance.commentaire}\" du restaurant \"{instance.noRestaurant.nomRestaurant}\" situé à \"{instance.noRestaurant.villeRestaurant}\""
            )
        else:
            Log.objects.create(
                user=user,
                action=f"{user.username} a supprimé ce commentaire: \"{instance.commentaire}\" du restaurant \"{instance.noRestaurant.nomRestaurant}\" situé à \"{instance.noRestaurant.villeRestaurant}\""
            )


@receiver(pre_save, sender=Commentaire)
def capture_old_data(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Commentaire.objects.get(pk=instance.pk)
        print(f"[DEBUG - pre_save] old instance: {old_instance}")

        old_data = {}
        new_data = {}

        if old_instance.commentaire != instance.commentaire:
            old_data["commentaire"] = old_instance.commentaire
            new_data["commentaire"] = instance.commentaire
            print(f"[DEBUG - pre_save] commentaire changé: {old_instance.commentaire} -> {instance.commentaire}")

        if old_instance.note != instance.note:
            old_data["note"] = old_instance.note
            new_data["note"] = instance.note
            print(f"[DEBUG - pre_save] note changée: {old_instance.note} -> {instance.note}")

        if old_instance.dateCommentaire != instance.dateCommentaire:
            old_data["dateCommentaire"] = DateFormat(old_instance.dateCommentaire).format('d/m/Y H:i')
            new_data["dateCommentaire"] = DateFormat(instance.dateCommentaire).format('d/m/Y H:i')
            print(f"[DEBUG - pre_save] date changée: {old_instance.dateCommentaire} -> {instance.dateCommentaire}")

        if old_instance.noRestaurant != instance.noRestaurant:
            old_data["noRestaurant"] = old_instance.noRestaurant.nomRestaurant
            new_data["noRestaurant"] = instance.noRestaurant.nomRestaurant
            print(f"[DEBUG - pre_save] restaurant changé: {old_instance.noRestaurant.nomRestaurant} -> {instance.noRestaurant.nomRestaurant}")

        if old_data:
            instance.old_data = old_data
            instance.new_data = new_data
            print(f"[DEBUG - pre_save] Stockage old_data dans instance: {old_data}")
        else:
            instance.old_data = None
            instance.new_data = None
            print("[DEBUG - pre_save] Aucune modification détectée.")

@receiver(pre_save, sender=Restaurant)
def capture_old_data_restaurant(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Restaurant.objects.get(pk=instance.pk)
        print(f"[DEBUG - pre_save Restaurant] old instance: {old_instance}")

        old_data = {}
        new_data = {}

        if old_instance.nomRestaurant != instance.nomRestaurant:
            old_data["nomRestaurant"] = old_instance.nomRestaurant
            new_data["nomRestaurant"] = instance.nomRestaurant
            print(f"[DEBUG - pre_save Restaurant] nomRestaurant changé: {old_instance.nomRestaurant} -> {instance.nomRestaurant}")

        if old_instance.villeRestaurant != instance.villeRestaurant:
            old_data["villeRestaurant"] = old_instance.villeRestaurant
            new_data["villeRestaurant"] = instance.villeRestaurant
            print(f"[DEBUG - pre_save Restaurant] villeRestaurant changé: {old_instance.villeRestaurant} -> {instance.villeRestaurant}")

        if old_instance.adresseRestaurant != instance.adresseRestaurant:
            old_data["adresseRestaurant"] = old_instance.adresseRestaurant
            new_data["adresseRestaurant"] = instance.adresseRestaurant
            print(f"[DEBUG - pre_save Restaurant] adresseRestaurant changé: {old_instance.adresseRestaurant} -> {instance.adresseRestaurant}")

        if old_data:
            instance.old_data = old_data
            instance.new_data = new_data
            print(f"[DEBUG - pre_save Restaurant] Stockage old_data dans instance: {old_data}")
        else:
            instance.old_data = None
            instance.new_data = None
            print("[DEBUG - pre_save Restaurant] Aucune modification détectée.")
