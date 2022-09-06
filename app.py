from flask import Flask,render_template,redirect,url_for,request
import pickle
import numpy as np


app = Flask(__name__)

model=pickle.load(open("final_model.pkl","rb"))

@app.route("/login")
@app.route("/")
def login():
        return render_template("name.html")
    

@app.route("/home",methods=["POST"])
def home():
    if len([str(x) for x in request.form.values() if x!=""])==3:
        return render_template("index.html",statement=[str(x) for x in request.form.values() if x!=""])
    else:
        return redirect(url_for("login"))
    

@app.route("/heart_risk")
def heart_risk():
    return render_template("heart_risk.html")

@app.route("/no_heart_risk")
def no_heart_risk():
    return render_template("no_heart_risk.html")

@app.route("/predict",methods=["POST"])
def predict():
    int_features = [float(x) for x in request.form.values()]
    if np.sum(int_features)==0.0:
        return render_template("index.html",error_statement1="Please fill in the form! You cannot submit the empty form.")
    else:
        final_features = np.array(int_features).reshape(1,-1)
        prediction = model.predict(final_features)
    if prediction==1:
        final_result = "heart_risk"
    else:
        final_result = "no_heart_risk"
    return redirect(url_for(final_result))

@app.route("/back")
def back():
    return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)