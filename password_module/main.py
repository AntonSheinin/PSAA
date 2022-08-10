import os
from celery import Celery

app = Celery('main', broker='pyamqp://user:bitnami@rabbitmq', backend='rpc://user:bitnami@rabbitmq')

def password_search(files_list: list, word: str) -> dict:

    files_with_password = {'task_name' : 'password', 'count' : 0, 'files' : []}

    for file_name in files_list:
        with open(file_name, encoding='utf8') as file:
            count = 0
            count = sum([line.count(word) for line in file])

            if count:
                files_with_password['files'].append({'file name' : file_name, 'count' : count})
                files_with_password['count'] += count

    return files_with_password

def get_files_list(directory: str) -> list:

    files_list = []
    for root, _, files in os.walk(directory):
        files_list.extend([os.path.join(root, file_name) for file_name in files])

    return files_list

@app.task(name='password')
def password() -> dict:
    return password_search(get_files_list('./theHarvester'), 'password')
