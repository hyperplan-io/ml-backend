from flask import Flask, g
import json
import falcon
import multiprocessing

import gunicorn.app.base


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class PredictionHandler():
    def __init__(self, project):
        self.project = project

    def on_get(self, req, resp): 
        resp.media = {"project": self.project.project_id}

class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

class MlRestApp():
    """

    """
    def __init__(self, projects):
        self.projects = projects

    def start(self):
        api = falcon.API()
        for project in self.projects:
            api.add_route('/{}'.format(project.project_id), PredictionHandler(project))
        options = {
            'bind': '%s:%s' % ('127.0.0.1', '8080'),
            'workers': number_of_workers(),
        }
        StandaloneApplication(api, options).run()
