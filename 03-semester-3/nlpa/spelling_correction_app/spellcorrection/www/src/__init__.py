from __future__ import annotations
import os
from email.message import Message
from urllib import request
from urllib.error import HTTPError
from flask import Flask, jsonify, redirect, url_for, render_template, request, abort
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from spellcorrection.configuration import conf
from spellcorrection.www import app_config
from spellcorrection.exception import SpellCorrectionException
from spellcorrection.model import SpellingCorrector



spellcorrection_app: Flask | None = None

HTTP_400_BAD_REQUEST = 400 
HTTP_404_NOT_FOUND = 404 
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_500_INTERNAL_SERVER_ERROR = 500 
HTTP_401_UNAUTHORIZED = 401


def create_file_serve_app(test_config=None, testing = False):
    app = Flask('file_serve_app', instance_relative_config= True, static_folder=conf.get('backend','corrected_file_path'))

    if not test_config:
        app.config["APP_NAME"] = "SpellCorrection File Server"
    else:
        app.config.from_mapping(test_config)

    app.config["TESTING"] = testing

    @app.route('/<string:corrected_file>',methods=['GET'])
    def corrected_file(corrected_file:str):
        return redirect(url_for('static',filename=corrected_file))
    return app

def create_app(test_config = None, testing = False):
    # console/dist is used to host the UI for the webserver
    app = Flask(__name__, 
                instance_relative_config = True, 
                static_url_path='', 
                static_folder='console-spellcorrection/dist', 
                template_folder='console-spellcorrection/dist')
    
    if not test_config:
        app.config.from_object(app_config)
    else:
        app.config.from_mapping(test_config)

    app.config["TESTING"] = testing

    cors = CORS(app,resources={r"/*":{"origins" : "*"}}, supports_credentials=True)

    @app.route("/", defaults={'path':''})
    @app.route("/<path:path>/")
    def serve(path):
        return render_template('index.html', api_url = conf.get('webserver','base_url'))
    
    @app.route('/correct', methods=['POST'])
    def correct():
        try:
            data = request.json
            default_model_type = conf.get('backend', 'model_type')
            model_type = data.get('model_type', default_model_type)
            text = data['text']
            #print("we are here: ", text)
            corrector = SpellingCorrector(model_type)
            corrected_text = corrector.correct_text(input_type = 'text', input_text = text)
            return jsonify({'corrected_text': corrected_text})
        except Exception as e:
            raise HTTPError(msg=f'text spelling correction failed with the error:\n{str(e)}',url='',code=500,hdrs=Message(),fp=None)
    
    @app.route('/correct_file', methods=['POST'])
    def correct_file():
        try:
            files = request.files
        except Exception as e:
            return jsonify('No file was given to be uploaded'),400
        try:
            file_upload_dir =  conf.get('backend', 'file_upload_path')
            corrected_file_dir = conf.get('backend', 'corrected_file_path')
            corrected_file_base_url = conf.get('webserver','base_url').rstrip('/') + '/output/'
            model_type = 'language_tool'
            corrector = SpellingCorrector(model_type)

            file_names = []
            corrected_files = {}
            for key,_ in files.items():
                file = files[key]
                filename=file.filename
                file_names.append(filename)
                input_file_path = os.path.join(file_upload_dir, filename)
                file.save(input_file_path)
                corrector.correct_text(input_type = 'file', file_path = input_file_path)
                corrected_files[filename] = f'{corrected_file_base_url}corrected_{filename}'

            return jsonify(corrected_files),201
        except Exception as e:
            raise HTTPError(msg=f'File spelling correction failed with the error:\n{str(e)}',url='',code=500,hdrs=Message(),fp=None)
        

    

    @app.errorhandler(SpellCorrectionException)
    def execution_not_found(e:SpellCorrectionException):
        return jsonify({"error" : str(e)}),400
    
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'This Sparkway page not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong.'}), HTTP_500_INTERNAL_SERVER_ERROR

    @app.errorhandler(HTTP_405_METHOD_NOT_ALLOWED)
    def handle_405(e):
        return jsonify({'error' : 'Please check the type of request'}),405
    
    @app.errorhandler(HTTP_400_BAD_REQUEST)
    def handle_400(e):
        return jsonify({'error' : 'Bad request'}), 400

    @app.errorhandler(HTTP_401_UNAUTHORIZED)
    def handle_401(e):
        return jsonify({"error" : "Unauthorized access"}),401
    
    return app
    

def cached_app(test_config=None, testing=False):
    """Return cached instance of SpellCorrection WWW app"""
    global spellcorrection_app
    if not spellcorrection_app:
        web_app = create_app(test_config=test_config, testing=testing)
        file_serve_app = create_file_serve_app()
        sparkway_app = DispatcherMiddleware(
            web_app, {
                '/output' : file_serve_app
            }
        )
    return sparkway_app