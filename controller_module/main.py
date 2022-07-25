#Home Assignment for PTBox.io

import logging
import messageBroker

from distutils.util import change_root
import json
import requests
from requests.auth import HTTPBasicAuth
import secrets
from random import random
from urllib import response
import redis
from bottle import route, run, template, request, static_file, error, default_app, response

import analize
import search_password

allowed_IP = ['127.0.0.1', '62.90.52.94', '94.130.136.116', '10.100.102.1']
menu_links = {'main-menu' : 'main_menu',
              'search' : 'search_password',
              'analize' : 'analize'}
             
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@route('/<url>', method=['GET','POST'])
def router(url):

    if (request.environ.get('HTTP_X_FORWARDED_FOR') is not None and request.environ.get('HTTP_X_FORWARDED_FOR') not in allowed_IP) or request.environ.get('REMOTE_ADDR') not in allowed_IP:
        print(request.environ.get('REMOTE_ADDR'))
        return(http_error_handling(403))

    session_id = request.get_cookie('sessionid')
    print(session_id)
    if session_id is None:
        session_id = secrets.token_urlsafe(8)
        response.set_cookie('sessionid', session_id)

    if url in menu_links:
        return(globals()[menu_links[url]](session_id))

    return(http_error_handling(404))

@route('/')
def router_wrapper():
        return router('main-menu')

def http_error_handling(code):

    if code == 403:
        return('access denied')
    if code == 404:
        return('page doesnt exist')

def main_menu(session):
    return template('templates/main_menu.tpl')

#def main():
#   run(server='gunicorn', host='10.100.102.6', port=8080)
    #run(host='127.0.0.1', port=8080)

app = default_app()

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

#if __name__ == '__main__':
#    logger.info("Controller module is running and listening...")
#    # TODO
