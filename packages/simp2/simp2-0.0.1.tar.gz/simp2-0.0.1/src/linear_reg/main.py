import sys
import os
import json
from flask import Flask, Response, request
import pickle
import numpy as np
from simple_linear_regr import SimpleLinearRegression
import traceback
from dotenv import load_dotenv

app = Flask(__name__)
model = None
api_keys = None


@app.route("/stream", methods=["POST"])
def stream_process():
    """
    Process a record
    Returns: predicted results or corresponding errors

    """
    # authentication
    key = request.headers.get('regression-api-key')
    if not key_authenticate(key):
        return Response(response=json.dumps({"results": "", "message": "Cannot authenticate"}), status=401)

    # get request data
    requested_data = request.json
    requested_data = np.array(requested_data["X_test"])

    # check model available
    if model is None:
        return Response(response=json.dumps({"results": "", "message": "Server cannot load model"}), status=500)

    # predict
    predict = model.predict(requested_data).item()

    return Response(response=json.dumps({"results": predict, "message": "Predict successfully"}), status=200)


@app.route("/batch", methods=["POST"])
def stream_proces():
    """
    Process a batch of records
    Returns: predicted results or corresponding errors

    """
    # authentication
    key = request.headers.get('regression-api-key')
    if not key_authenticate(key):
        return Response(response=json.dumps({"results": "", "message": "Cannot authenticate"}), status=401)

    # get request data
    requested_data = request.json
    requested_data = np.array(requested_data["X_test"])

    if model is None:
        return Response(response=json.dumps({"results": "", "message": "Server cannot load model"}), status=500)

    # predict
    predicts = model.predict(requested_data).flatten().tolist()

    return Response(response=json.dumps({"results": predicts, "message": "Predict successfully"}), status=200)


def load_model(path):
    """
    load saved serialized model from disk
    Args:
        path: path of model saved on disk

    Returns: loaded model

    """
    global model
    try:
        with open(path, 'rb') as raw_model:
            model = pickle.load(raw_model)
    except:
        print("Load model unsuccessfully !!!")
        traceback.print_exc()
        pass


def key_authenticate(key):
    """
    Authenticate requesting user
    Args:
        key: sent key from requesting user

    Returns: successful or not

    """
    if key in api_keys:
        return True
    return False


if __name__ == '__main__':
    # load configurations
    dotenv_path = os.path.join("configs", '.env')
    load_dotenv(dotenv_path)

    # get host, port
    host = os.environ.get('HOST', "localhost")
    port = int(os.environ.get('PORT', 8080))

    # get model information
    model_dir = os.environ.get('MODEL_DIR', "saved_model")
    model_name = os.environ.get('MODEL_NAME', "linear_model.dat")

    # load model key
    global api_keys
    api_keys = os.environ.get('API_KEYS').split(",")

    # load model
    load_model(os.path.join(model_dir, model_name))

    # start server
    app.run(debug=True, host=host, port=port)
