import random

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from spinner.models import Result as SpinnerResult


def index(req, template_prefix='spinner/'):
    """
    Display the Survey info
    """

    return render_to_response('%sindex.html' % template_prefix, {},
            context_instance=RequestContext(req))

def get_data(req, template_prefix='spinner/'):
    """
    Return all data as csv
    """
    response = render_to_response('%sresults.csv' % template_prefix, {
        'results': SpinnerResult.objects.all()})

    response['Content-Disposition'] = ("attachment; "
        "filename=spinner_survey_results.csv")

    return response
    #    mimetype='application/Excel')

def start_test(req, stage='start', template_prefix='spinner/'):
    """
    Display test with random values
    Get results from the POST if any
    Save the data
    """
    # check the survey response
    if req.method == 'POST':
        if req.POST.get('faster', False):
            # save data
            SpinnerResult.objects.create(
                xhr_duration=req.POST.get('xhr_duration'),
                spinner_delay_a=req.POST.get('spinner_delay_a'),
                spinner_delay_b=req.POST.get('spinner_delay_b'),
                faster=req.POST.get('faster'),
                broken=req.POST.get('broken', False)
            )
            return HttpResponseRedirect(reverse('spinner_thanks'))
        else:
            return HttpResponseRedirect(reverse('spinner_failed'))


    xhr_duration_set = ('0.2', '0.4', '0.6', '1.0', '1.5')
    spinner_delay_set = {
            '0.2': (0.0, 0.3),              # 0.3 will not show
            '0.4': (0.0, 0.2, 0.5),         # 0.5 will not show
            '0.6': (0.0, 0.2, 0.4, 0.7),    # 0.7 will not show
            '1.0': (0.0, 0.2, 0.4, 0.6),
            '1.5': (0.0, 0.2, 0.4, 0.6)
            }

    xhr_duration = random.choice(xhr_duration_set)
    spinner_delay_a = random.choice(spinner_delay_set[str(xhr_duration)])
    spinner_delay_b = random.choice(spinner_delay_set[str(xhr_duration)])
    xhr_duration = float(xhr_duration)

    return render_to_response('%stest.html' % template_prefix, {
        'xhr_duration': xhr_duration,
        'spinner_delay_a': spinner_delay_a,
        'spinner_delay_b': spinner_delay_b,
        'stage_template': '%s_%s.html' % (template_prefix, stage)
        }, context_instance=RequestContext(req))


def thanks(req):
    """
    Show thanks with ability to take the survey again
    """
    return start_test(req, stage='thanks')

def failure(req):
    """
    Show thanks with ability to take the survey again
    """
    return start_test(req, stage='error')
