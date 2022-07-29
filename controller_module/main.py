#Home Assignment for PTBox.io

from celery import Celery
import logging 
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

time.sleep(20)

app = Celery('main', broker='pyamqp://user:bitnami@rabbitmq', backend='rpc://user:bitnami@rabbitmq')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json')

tasks = []

def main():
    app.start()

    print('1. Search password', '\n', '2. Analyze files')
    choise = input('Enter choise : ')

    if choise == '1':
        tasks.append(app.send_task('password'))
    
    elif choise == '2':
        tasks.append(app.send_task('analyze'))

    else:
        print('wrong choice')

    for task in tasks:
        result = task.get()
        print('Received result:', result)

if __name__ == '__main__':
    logger.info("Controller module is running and listening...")
    main()
