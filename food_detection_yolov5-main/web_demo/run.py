# -*- coding: utf-8 -*-

from webapp import app
from flask_ngrok import run_with_ngrok
from flask import Flask, render_template, request

if __name__ == "__main__":
    # app.run(port=6006, debug=True)
    run_with_ngrok(app)
    app.run()

