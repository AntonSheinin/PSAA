import os
from collections import Counter
from celery import Celery

app = Celery('main', broker='pyamqp://user:bitnami@rabbitmq', backend='rpc://user:bitnami@rabbitmq')

def get_files_list(directory: str) -> dict:

    files_list = {'count' : 0, 'files' : []}

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file_name)[-1].lower()
            files_list['count'] += 1
            files_list['files'].append({'file_path' : file_path,
                                        'file_size' : file_size,
                                        'file_ext' : file_ext})

    return files_list

def files_list_analize(files_list : dict) -> dict:

    result = {'task_name' : 'analyze', 'ext' : {}, 'files' : []}
    ext_counter = Counter()

    files_list['files'].sort(key=lambda x: x['file_size'], reverse=True)
    result['files'] = files_list['files'][:10]

    for file in files_list['files']:
        ext_counter[file['file_ext']] += 1

    result['ext'] = [{k: v} for k, v in ext_counter.items()]

    return result

@app.task(name='analyze')
def analyze():

    return files_list_analize(get_files_list('./theHarvester'))