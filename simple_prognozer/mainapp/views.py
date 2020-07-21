from django.shortcuts import render
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from mainapp.models import Country, TimeSeries


def index(request):
    labels = []
    data_confirmed = []
    data_deaths = []
    data_recovered = []

    queryset = TimeSeries.objects.all().values('last_update').\
        annotate(Sum('confirmed'), Sum('deaths'), Sum('recovered'))

    for day in queryset:
        labels.append('{:%d/%m}'.format(day['last_update']))
        data_confirmed.append(day['confirmed__sum'] / 1000)
        data_deaths.append(day['deaths__sum'] / 1000)
        data_recovered.append(day['recovered__sum'] / 1000)

    countries = Country.objects.all()

    context = {
        'labels': labels,
        'data_confirmed': data_confirmed,
        'data_deaths': data_deaths,
        'data_recovered': data_recovered,
        'countries': countries,
    }
    return render(request, 'mainapp/index.html', context)


def country_page(request, pk):
    country = get_object_or_404(Country, pk=pk)
    countries = Country.objects.all()

    context = {
        'country_name': country.country,
        'countries': countries,
    }
    return render(request, 'mainapp/country_page.html', context)
