from pyexpat.errors import messages
from typing import List

import requests

from time import sleep
from src.constants import QueueStatus

base_url = '	https://belarusborder.by/info/monitoring-new?token=test&checkpointId=a9173a85-3fc0-424c-84f0-defa632481e4'


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


def AnQue():
    AnnuledCount = 0
    SummonedCount = 0

    AnnuledCarsNumber = []
    SummonedCarsNumber = []

    Queue = get_carLiveQueue()
    QueueLen = len(Queue)

    for car in Queue:
        if car['status'] == QueueStatus.ANNULLED.value:
            AnnuledCount += 1
            AnnuledCarsNumber.append(car['regnum'])
        if car['status'] == QueueStatus.SUMMONED_IN_PP.value:
            SummonedCount += 1
            SummonedCarsNumber.append(car['regnum'])
    return QueueLen, AnnuledCount, AnnuledCarsNumber, SummonedCount, SummonedCarsNumber


def tracking_car(car_regnum: str) -> str:
    if check_car_in_queue(car_regnum):
        message = get_car_info(car_regnum)
        return message
    else:
        message = f'Your car {car_regnum} is not in queue\n Tracking disable. Car not found'
        return message


def get_queue_info() -> str:
    QueueLen, AnnuledCount, AnnuledCarsNumber, SummonedCount, SummonedCarsNumber = AnQue()


    messages = (f"Queue Lenght = {QueueLen} \nAnnuled Count = {AnnuledCount} \nAnnuledCarsNumber = {AnnuledCarsNumber} "
                f"\nSummoned Count = {SummonedCount} \nSummonedCarsNumber = {SummonedCarsNumber}")

    return messages

