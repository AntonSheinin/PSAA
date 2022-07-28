#Home Assignment for PTBox.io test

from celery import Celery
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CELERY_QUEUES = {'search_queue': {'exchange' : 'search_queue', 'routing_key' : 'search_queue'},
                 'analyze_queue': {'exchange' : 'analyze_queue', 'routing_key' : 'analyze_queue'}}

CELERY_ROUTES = {
    'search': {'queue': 'search_queue', 'routing_key': 'search_queue'},
    'analyze': {'queue': 'analyze_queue', 'routing_key': 'analyze_queue'},
}

app = Celery('main', broker='amqp://guest@localhost//', backend='rpc://')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json')

def main():
    app.start()

    #search_result = search_entry_point()
    #print(search_result)

    analyze_result = analyze.delay()
    print(analyze_result)

if __name__ == '__main__':
    logger.info("Controller module is running and listening...")
