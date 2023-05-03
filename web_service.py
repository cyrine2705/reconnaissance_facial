import json
import os
import shutil
import flask
import werkzeug
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restplus import Api, Resource , fields
from werkzeug.datastructures import FileStorage
import face_rec
from decoupagevedio import decoupage
from trainning import trainig
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app=app, version='0.1', title='ApiV', description='',
    security='https',
    SWAGGER_SUPPORTED_SUBMIT_METHODS=['get', 'post', 'put', 'delete'], 
    SWAGGER_UI_REQUEST_HEADERS={'Content-Type': 'application/json'}, validate=True)

""" UPLOAD_DIRECTORY = "/unkownPic" """
@cross_origin("*")
@api.route("/training/")
class identifier(Resource):
    def get(self):
        trainig()



parser_video = api.parser()
parser_video.add_argument('file', location='files', type=FileStorage, required=True)
@cross_origin("*")
@api.route('/with-parser-video/parser-video/')

@api.expect(parser_video)
class WithParserResourcevideo(Resource):
    @api.doc(parser=parser_video)
    def post(self):
        data = flask.request.files['file']
        print(data)
        filename = werkzeug.utils.secure_filename(data.filename)
        print("\nReceived video File name : " + data.filename)
        saved_path = os.path.join("video", filename)
        data.save(saved_path)
        message=decoupeV.post(self,filename)
        return "video Uploaded Successfully"+ json.dumps(message)


class decoupeV(Resource):
    def post(self, title):
        print(title)
        data = request
        print(title)
        print(data)
        decoupage(title)







parser = api.parser()
parser.add_argument('file', location='files', type=FileStorage, required=True)
@api.route('/with-parser/parser/')
@api.expect(parser)
class WithParserResource(Resource):
    @api.doc(parser=parser)
    def post(self):
        data = flask.request.files['file']
        print(data)
        filename = werkzeug.utils.secure_filename(data.filename)
        print("\nReceived image File name : " + data.filename)
        saved_path = os.path.join("test", filename)
        data.save(saved_path)
        message=identifier.get(self)
        return "Image Uploaded Successfully"+ json.dumps(message)



class identifier(Resource):
    def get(self):
        for image_file in os.listdir("test"):
            full_file_path = os.path.join("test", image_file)

        print("Looking for faces in {}".format(image_file))

        # Find all people in the image using a trained classifier model
        # Note: You can pass in either a classifier file name or a classifier model instance
        predictions = face_rec.predict(full_file_path, model_path="trained_knn_model.clf")

        # Print results on the console
        list=[]
        for name, (top, right, bottom, left) in predictions:
            list.append(name)
            print("- Found {} at ({}, {})".format(name, left, top))

        # Display results overlaid on an image
        #face_rec.show_prediction_labels_on_image(os.path.join("test", image_file), predictions)

        """ if name.find("unknown") != "unknown": """
        
        print(list)
        if "unknown"  not in list and len(list)>0 :
            shutil.copy(os.path.join("test", image_file), 'picture/' + name)
            os.remove(os.path.join("test", image_file))
            return {"statu": True, "message": "found face ", "response": list}
        else:
            shutil.copy(os.path.join("test", image_file), 'unkownPic' )
            os.remove(os.path.join("test", image_file))
            return {"statu": False, "message": "found face ", "response": list}


if __name__ == "__main__":
    from waitress import serve
    port = int(os.environ.get('PORT', 8885))
    serve(app,port=port)