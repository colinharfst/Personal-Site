from django.shortcuts import render
from .models import Judge
import datetime
from datetime import timedelta
import sqlite3

def main(request):
    context = {}
    return render(request, 'pages/main.html', context)

def judge(request):
    
    #     # Make judge object and check if he homered
    #     jdg = Judge()
    #     hr_val = jdg.didJudgeHR()
    #     print("-----FUNC STATS-----")
    #     print(hr_val)
    #     print(jdg.lastGameVal)
    #     print(jdg.lastHRDate)
    
    try:
        # Get values from Judge's last game
        hr_stats = Judge.objects.get()
        # Maybe changes with daylight saving time
        hr_date_adjusted = hr_stats.lastHRDate - timedelta(hours=10)
        # print(datetime.datetime(hr_stats.lastHRDate) - timedelta(hours=5))
        print("-----DB STATS-----")
        print(hr_stats.lastGameVal)
        print(hr_date_adjusted)
    except:
        print("DB operation failed")
    
    # Make judge object and check if he homered
    jdg = Judge()
    hr_val = jdg.didJudgeHR()
    if (jdg.lastHRDate != None):
        jdg_hr_date_adjusted = jdg.lastHRDate - timedelta(hours=10)
    print("-----FUNC STATS-----")
    print(hr_val)
    print(jdg.lastGameVal)
    if (jdg.lastHRDate != None):
        print(jdg_hr_date_adjusted)

    context = {}
    
    # There was a game today and Judge didn't homer
    if (hr_val == 0):
        Judge.objects.all().delete()
        print('a')
        
        jdg.lastHRDate = hr_stats.lastHRDate
        print('b')
        jdg.save()
        print('c')
        
        context = {
            'did_judge_hr': hr_val,
            'lastGameVal': hr_val,
            #             'lastHRDate': jdg.lastHRDate.strftime("%b %-d, %Y")
            'lastHRDate': hr_date_adjusted.strftime("%B %-d, %Y")}

    # There was a game today and Judge did homer
    if (hr_val != 999):
        Judge.objects.all().delete()
    
        jdg.save()
        
        context = {
            'did_judge_hr': hr_val,
            'lastGameVal': hr_val,
            'lastHRDate': jdg_hr_date_adjusted.strftime("%B %-d, %Y")}
    
    # There wasn't a game today
    else:
        context = {
            'did_judge_hr': hr_val,
            'lastGameVal': hr_stats.lastGameVal,
            'lastHRDate': hr_date_adjusted.strftime("%B %-d, %Y")}
    return render(request, 'pages/judge.html', context)

def chess(request):
    context = {}
    return render(request, 'pages/chess.html', context)

def math(request):
    context = {}
    return render(request, 'pages/math.html', context)
