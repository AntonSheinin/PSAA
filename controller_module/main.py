#Home Assignment for PTBox.io

import logging 
import json
from celery import Celery
from kombu import Queue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Celery('main', broker='pyamqp://user:bitnami@rabbitmq', backend='rpc://user:bitnami@rabbitmq')

app.conf.task_queues = (Queue('password'), Queue('analyze'))

def main():

    tasks = []

    tasks.append(app.send_task('password', queue = 'password'))
    logger.info('password search task sent')

    tasks.append(app.send_task('analyze', queue = 'analyze'))
    logger.info('file analyze task sent')

    for task in tasks:
        result = task.get()
        task_name = result['task_name']
        logger.info('result for task %s received', task_name)
        with open('./theHarvester/' + task_name + '.json', 'w', encoding="utf8") as file:
            json.dump(result, file)
            logger.info('result for task %s saved to file %s.json', task_name, task_name)
   
if __name__ == '__main__':
    logger.info('Controller module is started...')
    main()
    logger.info('Controller module is stopped...')
