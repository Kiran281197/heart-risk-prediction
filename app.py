from flask import Flask,render_template,redirect,url_for,request
import pickle
import numpy as np


app = Flask(__name__)

model=pickle.load(open("final_model.pkl","rb"))

@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/heart_risk")
def heart_risk():
    return render_template("heart_risk.html")

@app.route("/no_heart_risk")
def no_heart_risk():
    return render_template("no_heart_risk.html")

@app.route("/submit",methods=["POST"])
def submit():
    int_features = [float(x) for x in request.form.values()]
    final_features = np.array(int_features).reshape(1,-1)
    prediction = model.predict(final_features)
    if prediction==1:
        final_result = "heart_risk"
    else:
        final_result = "no_heart_risk"
    return redirect(url_for(final_result))

if __name__=="__main__":
    app.run(debug=True)