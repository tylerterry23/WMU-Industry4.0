from django.shortcuts import render 

# Custom imports
from .models import Process, Product, ProductTime, StationHistory, Stations, Steps
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Sum, Func, F, Count, FloatField
import datetime
from datetime import timedelta


# define the dashboard view function
def dashboard(request):
    today_start = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_end = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    # Number of completed products from current session (datecompleted)
    num_completed = Product.objects.filter(Completed=True, StartTime__range=(today_start, today_end)).count()

    # Calculate the average cycle time
    avg_cycle_time_seconds = Product.objects.filter(Completed=True, StartTime__range=(today_start, today_end)).aggregate(avg_cycle_time=Avg(Func(F('TotalTime'), function='TIME_TO_SEC')))['avg_cycle_time']    

    avg_cycle_time = None
    if avg_cycle_time_seconds is not None:
        avg_cycle_time_seconds = float(avg_cycle_time_seconds)
        avg_cycle_time = datetime.time(minute=int(avg_cycle_time_seconds // 60), second=int(avg_cycle_time_seconds % 60))
        avg_cycle_time = avg_cycle_time.strftime('%M:%S')

    # Get the average time for each station


    # calculate the acceptance rate
    num_accepted = Product.objects.filter(Completed=True, Accepted=True, StartTime__range=(today_start, today_end)).count()
    acceptance_rate = (num_accepted / num_completed) * 100 if num_completed else None

    # calculate the number of assemblies in progress from 
    assemblies_in_progress = Product.objects.filter(Completed=False).count()

    # calculate the production rate (Amount to be made in a hour based on current rate using completed, accepted, in progress and total time)
    production_rate = Product.objects.filter(Completed=True, Accepted=True, StartTime__range=(today_start, today_end)).aggregate(production_rate=Avg(Func(F('TotalTime'), function='TIME_TO_SEC')))['production_rate']
    if production_rate is not None:
        production_rate = 3600 / production_rate
        production_rate = round(production_rate, 2)
    else:
        production_rate = 0

    # get the stations
    stations = Stations.objects.all()

    # Get the warnings
    warnings = get_warnings(today_start, today_end)
    
    context = {
        'num_completed': num_completed,
        'avg_cycle_time': avg_cycle_time,
        'acceptance_rate': acceptance_rate,
        'production_rate': production_rate,
        'assemblies_in_progress': assemblies_in_progress,
        'stations': stations,
        'warnings': warnings,
    }

    return render(request, 'dashboard.html', context=context)




def get_warnings(today_start, today_end):
    warnings = []
    
    # Check if any station is inactive
    inactive_stations = Stations.objects.filter(Active=False).count()
    if inactive_stations > 0:
        warnings.append({'message': f'{inactive_stations} stations are inactive', 'level': 1})
        
    # Check if any product is completed but not accepted from current session
    completed_not_accepted = Product.objects.filter(Completed=True, Accepted=False, StartTime__range=(today_start, today_end)).count()
    if completed_not_accepted > 0:
        warnings.append({'message': f'{completed_not_accepted} products are completed but not accepted', 'level': 2})

    return warnings

