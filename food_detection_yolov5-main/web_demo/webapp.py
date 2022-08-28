"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from PIL import Image
import pandas as pd 
import numpy as np
import torch
from flask import Flask, render_template, request, redirect

info_100g = pd.read_csv('/content/drive/MyDrive/project2/info_100g_l.csv')


app = Flask(__name__)

parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
parser.add_argument("--port", default=5000, type=int, help="port number")
args = parser.parse_args()

model = torch.hub.load('/content/drive/MyDrive/project2/yolov5/', 
    'custom', path='/content/drive/MyDrive/project2/best_l.pt', source='local')
model.eval()

@app.route("/", methods=["GET", "POST"])

def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=640)
        menu = results.pandas().xyxy[0]
        menu = menu['name']
        menu = list(np.array(menu.tolist()))

        #for i in menu :
        #  print(info[info['eng_name'].str.fullmatch(i)])
        
        info = pd.DataFrame(index=range(0,1), columns = {'음식명(kor_name)', '음식명(eng_name)', '에너지(kcal)', '탄수화물(g)', '당류(g)', '지방(g)', '단백질(g)'})
        for i,j in enumerate(menu) :
          info.loc[i] = info_100g[info_100g['음식명(eng_name)'].str.fullmatch(j)].reset_index().loc[0]
        info.to_html("/content/drive/MyDrive/project2/web_demo/templates/info.html")


        # for debugging
        # data = results.pandas().xyxy[0].to_json(orient="records")
        # return data

        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save("static/image0.jpg", format="JPEG")        
        #return redirect("static/test.csv")
        #return redirect("templates/index.html")
        return render_template("multispace.html")


    return render_template("index.html")

