#Home Assignment for PTBox.io

from celery import Celery
import logging 
import time
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

time.sleep(30)

tasks = []

app = Celery('main', broker='pyamqp://user:bitnami@rabbitmq', backend='rpc://user:bitnami@rabbitmq')

app.conf.update(task_serializer='json',
                accept_content=['json'],  
                result_serializer='json')

app.start()

#time.sleep(30)

tasks.append(app.send_task('password'))
print('password search task sent')

tasks.append(app.send_task('analyze'))
print('file analize task sent')

for task in tasks:
    result = task.get()
    with open('./output.json', 'w') as file:
        json.dump(result, file)
    print('Received result:', result)

#if __name__ == '__main__':
#    logger.info("Controller module is running and listening...")
#    app.start()
#    main()