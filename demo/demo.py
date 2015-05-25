# -*- coding: utf-8 -*-

import flask
from flask import Flask
from flask import abort
app = Flask(__name__)

import luigi
from bcube_demo_pipeline import MainWorkflow
from dlib.task_helpers import clear_directory
from dlib.call_solr import pull_from_solr


@app.route('/pipe')
def trigger_pipeline():
    '''
    run the pipeline
    '''
    doc_dir = 'bcube_demo/docs'

    pull_from_solr(doc_dir)
    task = MainWorkflow(doc_dir=doc_dir, yaml_file='configs/bcube_demo.yaml')
    luigi.interface.setup_interface_logging()
    sch = luigi.scheduler.CentralPlannerScheduler()
    w = luigi.worker.Worker(scheduler=sch)
    w.add(task)
    w.run()

    return ''


@app.route('/reset')
def reset():
    '''
    reset the pipeline (delete the intermediate files)
    TODO: drop from parliament?!
    '''
    dirs = ['docs', 'raw', 'identified', 'parsed', 'triples']
    for d in dirs:
        clear_directory(d)
    return

if __name__ == "__main__":
    app.run(debug=True)
