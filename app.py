from flask import Flask,jsonify,render_template,request,url_for
import pickle
import numpy as np

app=Flask(__name__)

with open("model.pkl","rb") as f:
    ml_model=pickle.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():

    data = request.form
    print("Data is :",data)

    age = float(data["age"])
    sex = int(data["sex"])
    bmi = float(data["bmi"])
    children = int(data["children"])
    smoker = int(data["smoker"])
    if data["region"] == "Southwest":
        ne,nw,se,sw=0,0,0,1
    if data["region"] == "Southeast":
        ne,nw,se,sw=0,0,1,0
    if data["region"] == "Northwest":
        ne,nw,se,sw=0,1,0,0
    if data["region"] == "Northeast":
        ne,nw,se,sw =1,0,0,0

    predictions = ml_model.predict([[age,sex,bmi,children,smoker,ne,nw,se,sw]])

    return jsonify({"Result":f"Predicted Insurance Charges are {predictions}"})

if __name__ == "__main__":
    app.run(debug=True)