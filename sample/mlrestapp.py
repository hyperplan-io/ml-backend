"""
    Ml rest app serves models on rest apis
"""
import json
import multiprocessing
import falcon
import gunicorn.app.base

def number_of_workers():
    """
        Computes the number of workers for gunicorn
    """
    return (multiprocessing.cpu_count() * 2) + 1


class PredictionHandler():
    """
        Prediction handler handles http request for model inference
    """
    def __init__(self, project, supported_formats):
        """
            Prediction handler constructor

            Keyword arguments:
            project -- the project to serve on this route
            supported_formats -- the http content types that are accepted
        """
        self.project = project
        self.supported_formats = supported_formats

    def get_project(self):
        """
            Returns the project served on this handler
        """
        return self.project

    def get_supported_formats(self):
        """
            Returns the formats supported by this handler
        """
        return self.project

    def on_post(self, req, resp):
        """
            Handles http POST requests
        """
        content_type = req.content_type
        if content_type in self.supported_formats:
            data = req.stream.read()
            features = []
            if content_type == 'application/json':
                features = json.loads(data)
            elif content_type == 'image/jpeg':
                features = [data]
            elif content_type == 'image/png':
                features = [data]

            prediction = self.project.predict(features, content_type, {})
            if prediction is None:
                resp.status = falcon.HTTP_BAD_REQUEST
                resp.media = {"error": "preprocessing did not return a result"}
            else:
                resp.status = falcon.HTTP_CREATED
                resp.media = {"project": self.project.project_id}
        else:
            resp.status = falcon.HTTP_UNSUPPORTED_MEDIA_TYPE
            resp.media = {
                "error": """
                    Type {} is not supported on project {}. 
                    If this type is incorrect, please check your Content-Type header
                        """.format(content_type, self.project.project_id)
            }

#pylint: disable=W0223
class StandaloneApplication(gunicorn.app.base.BaseApplication):
    """
        A Gunicorn standalone application
    """
    def __init__(self, app, options=None):
        """
            Constructor
        """
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        """
            Configuration loader
        """
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """
            Loads the configuration
        """
        return self.application

class MlRestApp():
    """
        A Machine Learning Restful Api
    """
    def __init__(self, projects):
        """
            The projects you want to serve

            Keyword arguments:
            projects --
            the tuples of projects you want to serve:
            (project, route, formats supported)
        """
        self.projects = projects

    def get_projects(self):
        """
            Returns the projects of the rest api
        """
        return self.projects

    def start(self):
        """
            Start the http server
        """
        api = falcon.API()
        for project, route, supported_formats in self.projects:
            api.add_route(route, PredictionHandler(project, supported_formats))
        options = {
            'bind': '%s:%s' % ('127.0.0.1', '8080'),
            'workers': number_of_workers(),
        }
        StandaloneApplication(api, options).run()
