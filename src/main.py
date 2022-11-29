from time import sleep

import requests

from src.constants import QueueStatus


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

    url = 'https://belarusborder.by/info/monitoring?checkpointId=7e46a2d1-ab2f-11ec-bafb-ac1f6bf889c1&token=bts47d5f-6420-4f74-8f78-42e8e4370cc4'

    r = requests.get(url=url, headers=headers)

    return r


def get_carLiveQueue(info):
    return info.json()['carLiveQueue']


def check_car_in_queue(queue, regnum) -> bool:
    if regnum in list(map(lambda x: x.get('regnum'), queue)):
        return True
    else:
        return False


def get_info_about_car():
    queue_info = get_info()
    car_live_queue_info = get_carLiveQueue(queue_info)

    return car_live_queue_info


def get_car_info(bot, message_id, regnum):
    prev_order_id = None
    while True:
        queue = get_info_about_car()
        for i in queue:
            if regnum in i['regnum']:
                if prev_order_id is None:
                    prev_order_id = i['order_id']
                elif prev_order_id != i['order_id']:
                    bot.send_message(message_id, f'Your position has been changed. New position {i["order_id"]}')

                if i['status'] == QueueStatus.SUMMONED_IN_PP.value:
                    bot.send_message(message_id, f'GAZU KURWA')
                    for _ in range(60):
                        bot.send_message(message_id, f'GAZU')
                        sleep(1)
                    bot.send_message(message_id, f'GAZUUUUU KURWA')
                    break
                break
        sleep(30)
