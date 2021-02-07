#< import
import sys
import os
from flask import Flask, request
from domino.core import log
from domino.application import Application
from domino.postgres import Postgres
    
app = Flask(__name__)
application = Application(os.path.abspath(__file__), framework='MDL')
POSTGRES = Postgres.Pool()
  
import responses.about
@app.route('/about', methods=['POST', 'GET'])
def _about():
    return application.response(request, responses.about.Response, None)
@app.route('/about.<fn>', methods=['POST', 'GET'])
def _about_fn(fn):
    return application.response(request, responses.about.Response, fn)

import pages.start_page
@app.route('/pages/start_page', methods=['POST', 'GET'])
def _pages_print_server():
    return application.response(request, pages.start_page.Page, None)
@app.route('/pages/start_page.<fn>', methods=['POST', 'GET'])
def _pages_print_server_fn(fn):
    return application.response(request, pages.start_page.Page, fn)
   
import pages.print_queue
@app.route('/pages/print_queue', methods=['POST', 'GET'])
def _pages_print_queue():
    return application.response(request, pages.print_queue.Page, None, [POSTGRES])
@app.route('/pages/print_queue.<fn>', methods=['POST', 'GET'])
def _pages_print_queue_fn(fn):
    return application.response(request, pages.print_queue.Page, fn, [POSTGRES])
        
import pages.print_templates
@app.route('/pages/print_templates', methods=['POST', 'GET'])
def _pages_print_templates():
    return application.response(request, pages.print_templates.Page, None, [POSTGRES])
@app.route('/pages/print_templates.<fn>', methods=['POST', 'GET'])
def _pages_print_templates_fn(fn):
    return application.response(request, pages.print_templates.Page, fn, [POSTGRES])

import pages.printers
@app.route('/pages/printers', methods=['POST', 'GET'])
def _pages_printers():
    return application.response(request, pages.printers.Page, None, [POSTGRES])
@app.route('/pages/printers.<fn>', methods=['POST', 'GET'])
def _pages_printers_fn(fn):
    return application.response(request, pages.printers.Page, fn, [POSTGRES])
 
import pages.add_printer
@app.route('/pages/add_printer', methods=['POST', 'GET'])
def _pages_add_printer():
    return application.response(request, pages.add_printer.Page, None, [POSTGRES])
@app.route('/pages/add_printer.<fn>', methods=['POST', 'GET'])
def _pages_add_printer_fn(fn):
    return application.response(request, pages.add_printer.Page, fn, [POSTGRES])
           
import responses.show
@app.route('/show', methods=['POST', 'GET'])
def _responses_file_show():
    return application.response(request, responses.show.Response, None, [POSTGRES])
@app.route('/show.<fn>', methods=['POST', 'GET'])
def _responses_show_fn(fn):
    return application.response(request, responses.show.Response, fn, [POSTGRES])
     
import responses.get_template
@app.route('/get_template', methods=['POST', 'GET'])
def _responses_get_template():
    return application.response(request, responses.get_template.Response, None, [POSTGRES])
@app.route('/get_template.<fn>', methods=['POST', 'GET'])
def _responses_get_template_fn(fn):
    return application.response(request, responses.get_template.Response, fn, [POSTGRES])

import responses.get_template_dataset
@app.route('/get_template_dataset', methods=['POST', 'GET'])
def _responses_get_template_dataset():
    return application.response(request, responses.get_template_dataset.Response, None, [POSTGRES])
@app.route('/get_template_dataset.<fn>', methods=['POST', 'GET'])
def _responses_get_template_dataset_fn(fn):
    return application.response(request, responses.get_template_dataset.Response, fn, [POSTGRES])
 
import responses.reg_printer
@app.route('/reg_printer', methods=['POST', 'GET'])
def _reg_printer(): 
    return application.response(request, responses.reg_printer.Response, None , [POSTGRES])
@app.route('/reg_printer.<fn>', methods=['POST', 'GET'])
def _reg_printer_fn(fn):
    return application.response(request, responses.reg_printer.Response, fn, [POSTGRES])

def navbar(page):    
    nav = page.navbar()
    nav.header('print_server', 'pages/start_page')
    nav.item('Очередь на печать', 'pages/print_queue')
    nav.item('Шаблоны отчетов', 'pages/print_templates')
    nav.item('Устройства печати', 'pages/printers')
application['navbar'] = navbar
 