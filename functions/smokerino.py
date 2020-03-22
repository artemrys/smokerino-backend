import json
import logging

import flask
from google.cloud import firestore

firestore_client = firestore.Client()


def get_cigarette(request: flask.Request) -> flask.Response:
    if request.method != "GET":
        return flask.make_response(flask.make_response("Only GET requests"),
                                   405)
    user_id = request.args.get("user_id")
    cigarette_ref = firestore_client.collection(f"cigarettes/{user_id}/smoked")
    smoked_cigarettes = len(list(cigarette_ref.get()))
    logging.info("User {user_id} asked about his progress")
    return flask.make_response(
        flask.Response(json.dumps({"smoked": smoked_cigarettes})), 200)


def add_cigarette(request: flask.Request):
    if request.method != "POST":
        return flask.make_response(flask.Response("Only POST requests"), 405)
    user_id = request.args.get("user_id")
    user_id_ref = firestore_client.collection("cigarettes").document(user_id)
    user_id_ref.set({
        "user_id": user_id,
    })
    cigarette_ref = user_id_ref.collection("smoked").document()
    cigarette_ref.set({
        "at": firestore.SERVER_TIMESTAMP,
    })
    logging.info(f"User {user_id} smoked")
    return flask.make_response(flask.Response("OK"), 200)
