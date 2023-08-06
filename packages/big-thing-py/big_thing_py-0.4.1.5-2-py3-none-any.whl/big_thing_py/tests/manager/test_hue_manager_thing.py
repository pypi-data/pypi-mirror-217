import big_thing.utils as utils
from big_thing.utils import (
    encode_MQTT_message,
    decode_MQTT_message,
    dict_to_json_string,
    json_string_to_dict,
    get_current_time,
    type_converter,
    get_function_return_type,
    get_function_parameter,
    get_ip_from_url)

from big_thing.MXTag import MXTag
from big_thing.MXArgument import MXArgument
from big_thing.MXFunction import MXFunction
from big_thing.MXValue import MXValue
from big_thing.MXThing import MXThing
from sample_class.manager_client.HueManagerClient import MXHueManagerClient

from typing import *
from threading import Thread, Event, current_thread
from functools import singledispatch
from queue import Queue
from time import sleep, time
import json

from termcolor import colored, cprint
import paho.mqtt.client as mqtt
import pytest


def test_manager_client_init():
    client = MXHueManagerClient(ip='iotdev.snu.ac.kr', port=11883,
                                bridge_ip='http://147.46.114.24/api/', bridge_port=80,
                                user_key='L-idzo6XFfRVA-DzXyA66xKzi-KxIJA75neakYyS',
                                refresh_cycle=5,)
    assert client.setup()
    assert client.run(timeout=5)
    assert client.wrapup()


cnt = 3


def test_manager_client_run():
    global cnt

    client = MXHueManagerClient(ip='iotdev.snu.ac.kr', port=11883,
                                bridge_ip='http://147.46.114.24/api/', bridge_port=80,
                                user_key='L-idzo6XFfRVA-DzXyA66xKzi-KxIJA75neakYyS',
                                refresh_cycle=5,)
    assert client.setup()

    execute_event: Event = Event()
    execute_thread: Thread = Thread(
        target=client.run, daemon=True, kwargs={'stop_event': execute_event, 'timeout': 20, })
    execute_thread.start()
    base_run_time = 2

    sleep(1)

    on_func_test = []
    for i in range(0, 3):
        on_func_test.append({'time': base_run_time,
                             'published': False,
                             'topic': f'MT/on/{client._thing_list[i].get_name()}',
                             'payload': dict_to_json_string(
                                 {
                                     "scenario": "scenario_name",
                                     "arguments":
                                     [
                                     ]
                                 })
                             })
    base_run_time += 0.5

    off_func_test = []
    for i in range(0, 3):
        off_func_test.append({'time': base_run_time,
                              'published': False,
                              'topic': f'MT/off/{client._thing_list[i].get_name()}',
                              'payload': dict_to_json_string(
                                  {
                                      "scenario": "scenario_name",
                                      "arguments":
                                      [
                                      ]
                                  })
                              })
    base_run_time += 0.5

    set_brightness_func_test = []
    for i in range(0, 3):
        set_brightness_func_test.append({'time': base_run_time,
                                         'published': False,
                                         'topic': f'MT/set_brightness/{client._thing_list[i].get_name()}',
                                         'payload': dict_to_json_string(
                                             {
                                                 "scenario": "scenario_name",
                                                 "arguments":
                                                 [
                                                     {
                                                         "order": 0,
                                                         "value": 50
                                                     }
                                                 ]
                                             })
                                         })
    base_run_time += 0.5

    # set_color_func_test = {'time': 3.5,
    #                        'published': False,
    #                        'topic': f'MT/set_color/{client._thing_list[5].get_name()}',
    #                        'payload': dict_to_json_string(
    #                            {
    #                                "scenario": "scenario_name",
    #                                "arguments":
    #                                [
    #                                    {
    #                                        "order": 0,
    #                                        "value": 50
    #                                    }
    #                                ]
    #                            })
    #                        }

    test_func_list: dict = on_func_test + off_func_test + set_brightness_func_test

    cnt = len(test_func_list)

    def on_message(client, userdata: Callable, msg: mqtt.MQTTMessage):
        global cnt
        topic, payload = decode_MQTT_message(msg)
        if 'TM/RESULT/FUNCTION/' in topic:
            cnt -= 1
            print(f'cnt : {cnt}')

    dummy_client = mqtt.Client(userdata=cnt)
    dummy_client.on_message = on_message
    dummy_client.connect(get_ip_from_url('iotdev.snu.ac.kr'), 11883)
    for func in test_func_list:
        function_name: str = func['topic']
        function_name = function_name.split('/')[1]
        for i in range(0, 3):
            dummy_client.subscribe(
                f'TM/RESULT/FUNCTION/{function_name}/{client._thing_list[i].get_name()}')
    dummy_client.loop_start()

    cur_time = get_current_time()
    timeout = 20

    while get_current_time() - cur_time < timeout:
        if client._alive_event.is_set():
            assert client.wrapup()
            assert False, 'alive_event set'
        if client._register_event.is_set():
            assert client.wrapup()
            assert False, 'register_event set'
        if client._value_publish_event.is_set():
            assert client.wrapup()
            assert False, 'value_publish_event set'
        if client._function_actuate_event.is_set():
            assert client.wrapup()
            assert False, 'function_actuate_event set'
        if client._function_actuate_result_event.is_set():
            assert client.wrapup()
            assert False, 'function_actuate_result_event set'
        if client._receive_message_event.is_set():
            assert client.wrapup()
            assert False, 'handle_recv_mqtt_event set'

        for func in test_func_list:
            if (get_current_time() - cur_time) > func['time'] and not func['published']:
                dummy_client.publish(
                    func['topic'], func['payload'])
                func['published'] = True

        if cnt == 0:
            print('function actuate test pass!!!')
            execute_event.set()
            assert client.wrapup()
            break
    else:
        assert False, 'timeout...'
