from typing import List

import requests

from time import sleep
from src.constants import QueueStatus

base_url = 'https://belarusborder.by/info/monitoring?checkpointId=7e46a2d1-ab2f-11ec-bafb-ac1f6bf889c1&token=bts47d5f-6420-4f74-8f78-42e8e4370cc4'


def get_info():

    headers = {
                "Accept" : "application/json, text/plain, */*",
                "Accept-Encoding" : "gzip, deflate, br",
                "Accept-Language" : "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Host": "belarusborder.by",
                "Origin": "https://mon.declarant.by/",
                "Referer": "https://mon.declarant.by/",
                "Sec-Fetch-Dest" : "empty",
                "Sec-Fetch-Mode" : "cors",
                "Sec-Fetch-Site" : "cross-site",
                "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
    }

    url = base_url

    response = requests.get(url=url, headers=headers)
    return response


def get_carLiveQueue() -> List:
    return get_info().json()['carLiveQueue']


def check_car_in_queue(regnum) -> bool:
    carLiveQueue = get_carLiveQueue()
    if regnum in list(map(lambda x: x.get('regnum'), carLiveQueue)):
        return True
    else:
        return False


def get_car_info(car_regnum) -> str:
    prev_order_id = -1
    while True:
        carLiveQueue = get_carLiveQueue()

        for car in carLiveQueue:
            if car_regnum in car['regnum']:
                if prev_order_id == -1:
                    prev_order_id = int(car['order_id'])
                    message = f"Your started position {car['order_id']}"
                    return message
                elif prev_order_id != int(car['order_id']):
                    message = f'Your position has been changed. New position {car["order_id"]}'
                    if car['status'] == QueueStatus.SUMMONED_IN_PP.value:
                        message = f'GAZU KURWA'
                        return message
                    return message
                else:
                    message = f'Car {car_regnum} not found in queue'
                    return message
        sleep(30)


def tracking_car(car_regnum: str) -> str:
    if check_car_in_queue(car_regnum):
        message = get_car_info(car_regnum)
        return message
    else:
        message = f'Your car {car_regnum} is not in queue\n Tracking disable. Car not found'
        return message

