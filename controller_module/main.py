import logging 
import json
from celery import Celery
from kombu import Queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

app = Celery('main', broker='pyamqp://user:bitnami@rabbitmq', backend='rpc://user:bitnami@rabbitmq')

app.conf.task_queues = (Queue('password'),
                        Queue('analyze'))

def result_saving(result: dict) -> None:
    task_name = result['task_name']
    logger.info(f'result for task {task_name} received')
    with open('./theHarvester/' + task_name + '.json', 'w', encoding='utf8') as file:
        json.dump(result, file)
        logger.info(f'result for task {task_name} saved to file {task_name}.json') 

def main():

    logger.info('Controller module is started...')

    logger.info('password search task sent')
    result_saving(app.send_task('password', queue = 'password').get())

    logger.info('files analyze task sent')
    result_saving(app.send_task('analyze', queue = 'analyze').get())

    logger.info('Controller module is stopped...')

if __name__ == '__main__':
    main()
    
