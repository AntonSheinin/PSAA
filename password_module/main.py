import logging
from celery import Celery
import os
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

time.sleep(15)

app = Celery('main', broker='pyamqp://user:bitnami@rabbitmq', backend='rpc://user:bitnami@rabbitmq')

def password_search(files_list, word):

    files_with_password = {'task_name' : 'password', 'count' : 0, 'files' : []}
    count = 0

    for file_name in files_list:
        with open(file_name) as file:
            count = 0
            for line in file:
                if line.count(word) > 0:
                    count += line.count(word)

            if count > 0 :
                files_with_password['files'].append({'file name' : file_name, 'count' : count})
                files_with_password['count'] += count

    return files_with_password

def get_files_list(directory):

    files_list = []
    for root, directories, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            files_list.append(file_path)

    return files_list

@app.task(name='password')
def password():
    
    #files_list = get_files_list('./theHarvester')

    #result = password_search(files_list, 'password')

    return password_search(get_files_list('./theHarvester'), 'password')