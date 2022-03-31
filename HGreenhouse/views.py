
from asyncio import FastChildWatcher
from django.shortcuts import HttpResponse
from django.http import JsonResponse

import json
import time

from HModules import HMySQL

sql = HMySQL.HSQL('HGreenhouse')

def index(request):
    return HttpResponse('这不是你该来的地方')

def set_hconfig(change_info: dict) -> bool:
    with open('HModules/thresholds', encoding='utf8') as f: hconfig = json.loads(f.readline())
    for k, v in change_info:
        if k in hconfig: hconfig[k] = v
    with open('HModules/thresholds_reset', encoding='utf8') as f: f.write(json.dumps(hconfig))
    return True

def set_temperature(request):
    rdata = dict()
    rdata['temperature'] = float(request.POST['num'][0])
    set_hconfig(rdata)
    rdata['state'] = 'ok'
    return JsonResponse(rdata)

def set_humidity(request):
    rdata = dict()
    rdata['humidity'] = int(request.POST['num'][0])
    set_hconfig(rdata)
    rdata['state'] = 'ok'
    return JsonResponse(rdata)

def set_light(request):
    rdata = dict()
    rdata['light'] = int(request.POST['num'][0])
    set_hconfig(rdata)
    rdata['state'] = 'ok'
    return JsonResponse(rdata)

def set_water(request):
    rdata = dict()
    rdata['water_auto'] = False
    rdata['water_state'] = bool(request.POST['status'][0])
    set_hconfig(rdata)
    rdata['state'] = 'ok'
    return JsonResponse(rdata)

def set_curtain(request):
    rdata = dict()
    rdata['curtain_auto'] = False
    rdata['curtain_state'] = bool(request.POST['status'][0])
    set_hconfig(rdata)
    rdata['state'] = 'ok'
    return JsonResponse(rdata)

def get_data(request):
    print(f"get_data = {request.GET}")
    rdata = dict()
    rdata['pid'] = request.GET['houseNum'][0]
    if 'startTime' in request.GET and 'endTime' in request.GET:
        rdata['start_date'] = request.GET['startTime']
        rdata['end_date'] = request.GET['endTime']
    else:
        rdata['start_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 24*3600))
        rdata['end_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    rdata['data_type'] = 'dht'
    dht_data = sql.get_data(rdata)
    rdata['data_type'] = 'light'
    light_data = sql.get_data(rdata)
    return JsonResponse({'state': 'ok', 'dht_data': dht_data, 'light_data': light_data})

def get_state(request):
    with open('HModules/thresholds', encoding='utf8') as f: hconfig = json.loads(f.readline())
    rdata = hconfig
    rdata['pid'] = request.GET['houseNum'][0]
    rdata['state'] = 'ok'
    return JsonResponse(rdata)

