#Home Assignment for PTBox.io

import queue
from celery import Celery
from kombu import Queue
import logging 
import time
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

time.sleep(15)

app = Celery('main', broker='pyamqp://user:bitnami@rabbitmq', backend='rpc://user:bitnami@rabbitmq')

app.conf.task_queues = (Queue('password', routing_key='password'),
                        Queue('analyze', routing_key='analyze'))

#app.conf.update(result_serializer='json')

def main():

    tasks = []

    tasks.append(app.send_task('password', queue = 'password'))
    logger.info('password search task sent')

    tasks.append(app.send_task('analyze', queue = 'analyze'))
    logger.info('file analyze task sent')

    for task in tasks:
        result = task.get()
        task_name = result['task_name']
        logger.info('result for task' + task_name + 'received')
        with open('./theHarvester/' + task_name + '.json', 'w') as file:
            json.dump(result, file)
            logger.info('result for task' + task_name + 'saved to file ' + task_name + '.json')
        
if __name__ == '__main__':
    logger.info('Controller module is started...')
    main()
