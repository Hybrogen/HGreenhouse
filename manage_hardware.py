#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json
import time

def hlog(msg):
    logTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(f"{logTime} - {msg}")

def check_file(f_type: str, f_name: str, content: str = "{}"):
    if f_type == 'dir' and not os.path.isdir(f_name):
        if os.path.isfile(f_name): raise Exception(f"已存在同名文件 [{f_name}]，请检查系统所需文件夹路径是否被占用")
        else: os.mkdir(f_name)
    elif f_type == 'file' and not os.path.isfile(f_name):
        if os.path.isdir(f_name): raise Exception(f"已存在同名文件夹 [{f_name}]，请检查系统所需文件路径是否被占用")
        else:
            with open(f_name, 'w', encoding = 'utf8') as f: f.write(content)

HARDMODULEDIR = "HModules"
check_file('dir', HARDMODULEDIR)

thresholds = {
        'temperature': 24,
        'humidity': 80,
        'light': 5,
        'curtain_auto': True,
        'curtain_state': True,
    }

THRESHOLDS = f"{HARDMODULEDIR}/thresholds"
check_file('file', THRESHOLDS, json.dumps(thresholds))

PORTID = 1

def reset_threshold(first_init: bool = False):
    if os.path.isfile(THRESHOLDS + '_reset'):
        with open(THRESHOLDS + '_reset', encoding = 'utf8') as f:
            thresholds = json.loads(f.readline())
        os.rename(THRESHOLDS + '_reset', THRESHOLDS)
        return
    if first_init and os.path.isfile(THRESHOLDS):
        with open(THRESHOLDS, encoding = 'utf8') as f:
            thresholds = json.loads(f.readline())

def update_threshold_file():
    with open(THRESHOLDS, 'w', encoding = 'utf8') as f: f.write(json.dumps(thresholds))

################################## 初始化各个模块 ##################################
from HModules import HActuator, HMySQL, HSensors

sql = HMySQL.HSQL('HGreenhouse')
s_light = HSensors.IOSENSOR(5)
s_dht = HSensors.DHT(23, 'DHT22')
a_curtain = HActuator.SteeppingMOTOR([6, 13, 19, 26])
a_water = HActuator.HRELAY(24)

################################  定义各个功能模块  ################################

def module_1_autoWater() -> int:
    start_run_time = time.time()
    reset_threshold()
    data = s_dht.check()
    if data.get('state') == 'error': return
    data['pid'] = PORTID
    sql.dht_save(data)
    humidity, temperature = data['humidity'], data['temperature']

    hlog(f"检测到温湿度数据: data = {data}")
    if humidity < thresholds['humidity'] or temperature > thresholds['temperature']:
        a_water.run(True)
        return 10 - int(time.time() - start_run_time)
    a_water.run(False)
    return 600 - int(time.time() - start_run_time)

def module_2_autoCurtain() -> int:
    start_run_time = time.time()
    reset_threshold()
    data = s_light.check()
    # 自动模式 - 如果检测状态和当前状态不同，窗帘活动并更新状态
    if thresholds['curtain_auto']:
        if thresholds['curtain_state'] != data:
            a_curtain.run(data)
            thresholds['curtain_state'] = data
            update_threshold_file()
    # 手动模式 - 如果检测状态与手动设定状态不同，活动窗帘
    # 并将窗帘重置为自动模式
    else:
        thresholds['curtain_auto'] = True
        if thresholds['curtain_state'] != data:
            a_curtain.run(thresholds['curtain_state'])
            thresholds['curtain_state'] = data
        update_threshold_file()

    hlog(f"检测到光照度数据: data = {data}")
    return 600- int(time.time() - start_run_time)

def main():
    reset_threshold(True)
    modules_run_info = {
            '1_autoWater': {
                'last_run_time': time.time(),
                'run_interval': 6,
            },
            '2_autoCurtain': {
                'last_run_time': time.time(),
                'run_interval': 6,
            },
        }
    while True:
        for module, run_info in modules_run_info.items():
            time.sleep(1)
            if int(time.time() - run_info['last_run_time']) > run_info['run_interval']:
                modules_run_info[module]['run_interval'] = eval(f"module_{module}")()
                run_info['last_run_time'] = time.time()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        hlog('智能温室大棚硬件系统停止工作')
