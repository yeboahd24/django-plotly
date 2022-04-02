from django.shortcuts import render
import plotly.express as px
import pandas as pd
from core.forms import DateForm
from core.models import CO2

# Create your views here.
def chart(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    co2 = CO2.objects.all()
    if start:
        co2 = co2.filter(date__gte=start)
    if end:
        co2 = co2.filter(date__lte=end)

    fig = px.line(
        x=[c.date for c in co2],
        y=[c.average for c in co2],
        title="CO2 PPM",
        labels={'x': 'Date', 'y': 'CO2 PPM'}
    )

    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, 'core/chart.html', context)



# Pie chart

def pie(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    df = CO2.objects.all()[:3]

    frame = pd.DataFrame(
        {
            'date': [c.date for c in df],
            'average': [c.average for c in df]
        }
    )

   
    fig = px.pie(
        frame,
        values='average',
        names='date',
        title='CO2 PPM',
    )


    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, 'core/chart.html', context)