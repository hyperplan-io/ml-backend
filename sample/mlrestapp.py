import json
import falcon
import multiprocessing
import gunicorn.app.base

from feature_type import FeatureType

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class PredictionHandler():
    def __init__(self, project):
        self.project = project

    def on_post(self, req, resp): 
        content_type = req.content_type
        data = req.stream.read()
        features = []
        features_type = None
        if content_type == 'application/json':
            features = json.loads(data)
            features_type = FeatureType.JSON 
        elif content_type == 'image/jpeg':
            features = [data]
            features_type= FeatureType.JPEG
        elif content_type == 'image/png':
            features = [data]
            features_type= FeatureType.PNG

        if self.project.supports_type(features_type):
            try:
                prediction = self.project.predict(features, features_type, {})
                if prediction is None:
                    resp.status = falcon.HTTP_BAD_REQUEST
                    resp.media = {"error": "preprocessing did not return a result"}
                else:
                    resp.status = falcon.HTTP_CREATED
                    resp.media = {"project": self.project.project_id}
            except Exception as e:
                resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
                resp.media = {"error": "blablabla"}
        else:
            resp.status = falcon.HTTP_UNSUPPORTED_MEDIA_TYPE
            resp.media = {"error": "Type {} is not supported on project {}. If this type is incorrect, please check your Content-Type header".format(content_type, self.project.project_id)}

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
