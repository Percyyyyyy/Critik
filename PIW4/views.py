import logging
from django.views.generic import TemplateView
import json
from restaurants.models import Log

class AccueilView(TemplateView):
    template_name = "accueil.html"
    
class AdministrationView(TemplateView):
    template_name = 'admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logs = Log.objects.all().order_by('-timestamp')[:100]

        for log in logs:
            try:
                log.old_data_dict = json.loads(log.old_data) if log.old_data and log.old_data.strip().startswith('{') else {}
            except Exception as e:
                logging.error(f"[ADMIN VIEW] Erreur old_data log {log.id}: {e}")
                log.old_data_dict = {}

            try:
                log.new_data_dict = json.loads(log.new_data) if log.new_data and log.new_data.strip().startswith('{') else {}
            except Exception as e:
                logging.error(f"[ADMIN VIEW] Erreur new_data log {log.id}: {e}")
                log.new_data_dict = {}

            log.changes = []
            if log.old_data_dict and log.new_data_dict:
                for key in log.old_data_dict:
                    old_val = log.old_data_dict.get(key, '')
                    new_val = log.new_data_dict.get(key, '')
                    if old_val != new_val:
                        log.changes.append(f"{key} : '{old_val}' --> '{new_val}'")


        context['logs'] = logs
        return context