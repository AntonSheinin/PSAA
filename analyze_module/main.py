import logging
import os
from collections import Counter
from celery import Celery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Celery('analyze_module', backend='ampq://', broker='pyamqp://', include=['analyze_module.main'])

def get_files_list(directory):

    files_list = {'count' : 0, 'files' : []}

    for root, directories, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file_name)[-1].lower()
            files_list['count'] += 1
            files_list['files'].append({'file_path' : file_path,
                                        'file_size' : file_size,
                                        'file_ext' : file_ext})

    return files_list

def files_list_analize(files_list):

    result = {'ext' : {}, 'files' : []}
    ext_counter = Counter()

    files_list['files'].sort(key=lambda x: x['file_size'], reverse=True)

    for i in range(10):
        result['files'].append(files_list['files'][i])

    for file in files_list['files']:
        ext_counter[file['file_ext']] += 1

    result['ext'] = [{k: v} for k, v in ext_counter.items()]

    return result

def main():
    app.start()

    #files_list = get_files_list("d:/Private/Phyton/PSAA/TheHarvester")

    #result = files_list_analize(files_list)

if __name__ == '__main__':
    logger.info("Analyze module is listening...")
    main()
