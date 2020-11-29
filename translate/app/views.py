from app import app
from flask import request, jsonify
from data import translator
import os
import time


@app.route("/api/v1/translate", methods=["GET"])
def translate():
    src = request.args.get("src", default="default", type=str)
    tgt = request.args.get("tgt", default="default", type=str)
    text = request.args.get("text", default="default", type=str)
    return translator.translate(src, tgt, text)