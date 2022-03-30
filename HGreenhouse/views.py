
from django.shortcuts import HttpResponse
from django.http import JsonResponse

import json

from HModules import HMySQL

sql = HMySQL.HSQL('HGreenhouse')

def index(request):
    return HttpResponse('自定义一些文本')

def datad(request):
    data = {'数据是这样返回的':'通过一个解析成json的字典对象'}
    # 常用的httpResponse，在返回数据的时候需要把字典解析成json"字符串"并且指定返回的文本类型
    return HttpResponse(json.dumps(data), content_type='application/json')
    # 也可以使用HttpResponse的一个子类JsonResponse，记得在头文件里引入对应的类
    # 使用JsonResponse可以直接返回字典对象，而不用再通过json库进行转换
    return JsonResponse(data)

def get_home(request):
    homes = sql.get_ports()
    return JsonResponse(homes)

def set_temperature(request):
    with open('HModules/thresholds', encoding='utf8') as f: hconfig = json.loads(f.readline())
    hconfig['temperature'] = float(request.GET['num'])
    with open('HModules/thresholds_reset', encoding='utf8') as f: f.write(json.dumps(hconfig))
    return JsonResponse({'state': 'ok', 'temperature': hconfig['temperature']})

def set_humidity(request):
    with open('HModules/thresholds', encoding='utf8') as f: hconfig = json.loads(f.readline())
    hconfig['humidity'] = int(request.GET['num'])
    with open('HModules/thresholds_reset', encoding='utf8') as f: f.write(json.dumps(hconfig))
    return JsonResponse({'state': 'ok', 'humidity': hconfig['humidity']})

def set_light(request):
    with open('HModules/thresholds', encoding='utf8') as f: hconfig = json.loads(f.readline())
    hconfig['light'] = int(request.GET['num'])
    with open('HModules/thresholds_reset', encoding='utf8') as f: f.write(json.dumps(hconfig))
    return JsonResponse({'state': 'ok', 'light': hconfig['light']})

def set_water(request):
    with open('HModules/thresholds', encoding='utf8') as f: hconfig = json.loads(f.readline())
    hconfig['water_auto'] = false
    hconfig['water_state'] = bool(request.get['status'])
    with open('hmodules/thresholds_reset', encoding='utf8') as f: f.write(json.dumps(hconfig))
    return jsonresponse({'state': 'ok', 'waterRunMode': 'manual', 'waterState': hconfig['water_state']})

def set_curtain(request):
    with open('HModules/thresholds', encoding='utf8') as f: hconfig = json.loads(f.readline())
    hconfig['curtain_auto'] = false
    hconfig['curtain_state'] = bool(request.get['status'])
    with open('HModules/thresholds_reset', encoding='utf8') as f: f.write(json.dumps(hconfig))
    return jsonresponse({'state': 'ok', 'curtainRunMode': 'manual', 'curtainState': hconfig['curtain_state']})

def get_data(request):
    thdata = sql.
