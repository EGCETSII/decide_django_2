import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods

from django.template.defaulttags import register
from statistics import mean, median, stdev, variance

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def get_statistics_from_voting(voting):
    res = list() 
    # [{'data': 
    #   {
    #       'name': '', 
    #       'value': 0
    #   }
    # }]
    data = [voto['postproc'] for voto in voting['postproc']]
    media = mean(data)
    mediana = median(data)
    deviation = stdev(data)
    varianza = variance(data)
    
    res.append({'name': 'Media', 'value': round(media, 2)})
    res.append({'name': 'Mediana', 'value': round(mediana, 2)})
    res.append({'name': 'Desviación media', 'value': round(deviation, 2)})
    res.append({'name': 'Varianza', 'value': round(varianza, 2)})
    # Añadir más tarde correlación entre grupos
    return res

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0].copy())
            context['statistics'] = get_statistics_from_voting(r[0].copy())
        except:
            raise Http404

        return context
