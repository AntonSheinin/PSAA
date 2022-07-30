#Home Assignment for PTBox.io

import queue
from celery import Celery
from kombu import Queue
import logging 
import time
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

time.sleep(30)



app = Celery('main', broker='pyamqp://user:bitnami@rabbitmq', backend='rpc://user:bitnami@rabbitmq')


app.conf.task_queues = (Queue('password', routing_key='password'),
                        Queue('analyze', routing_key='analyze'))

app.conf.update(result_serializer='json')

def main():

    tasks = []

    tasks.append(app.send_task('password', queue = 'password'))
    print('password search task sent')

    tasks.append(app.send_task('analyze', queue = 'analyze'))
    print('file analize task sent')

    for task in tasks:
        result = task.get()
        task_name = result['task_name']
        with open('./theHarvester/' + task_name + '.json', 'w') as file:
            json.dump(result, file)
        print('Received result:', result)

if __name__ == '__main__':
    logger.info("Controller module is running and listening...")
    main()
