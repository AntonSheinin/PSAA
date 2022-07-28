import logging
from celery import Celery
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Celery('password_module', backend='ampq://', broker='pyamqp://', include=['password_module.main'])

def password_search(files_list, word):

    files_with_password = {'count' : 0, 'files' : []}
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

def main():
    files_list = get_files_list('../theHarvester')

    result = password_search(files_list, 'password')

    print(result)

if __name__ == '__main__':
    logger.info("Password module is listening...")
    main()
