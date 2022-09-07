from flask import Flask,render_template,redirect,url_for,request,session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "super secret key"

model=pickle.load(open("final_model.pkl","rb"))


@app.route("/login/<a>")
@app.route("/")
def login(a=0):
    if a == 0:
        return render_template("name.html")
    else:
        return render_template("name.html",error_statement="Kindly fill all the details!")
    

@app.route("/home",methods=["POST"])
def home():
    firstname = str(request.form["firstname"])
    lastname = str(request.form["lastname"])
    preferredname = str(request.form["preferredname"])
    if (firstname!="") & (lastname!=""):
        if preferredname!="":
            session["preferred_name"] = preferredname
            return render_template("index.html",name=session["preferred_name"])
        else:
            session["first_name"] = firstname
            return render_template("index.html",name=session["first_name"])
    else:
        a=0
        return redirect(url_for("login",a=a+1))

@app.route("/heart_risk")
def heart_risk():
    if "preferred_name" in session:
        preferredname = session["preferred_name"]
        return render_template("heart_risk.html",nm=preferredname)
    else:
        firstname = session["first_name"]
        return render_template("heart_risk.html",nm=firstname)

        
@app.route("/no_heart_risk")
def no_heart_risk():
    firstname = session["first_name"]
    if "preferred_name" in session:
        preferredname = session["preferred_name"]
        return render_template("no_heart_risk.html",nm=preferredname)
    else:
        return render_template("no_heart_risk.html",nm=firstname)

@app.route("/predict",methods=["POST"])
def predict():
    int_features = [float(x) for x in request.form.values()]
    if np.sum(int_features)==0.0:
        if "preferred_name" in session:
            preferredname = session["preferred_name"]
            return render_template("index.html",error_statement1="Please fill in the form! You cannot submit the empty form.",name=preferredname)
        else:
            firstname = session["first_name"]
            return render_template("index.html",error_statement1="Please fill in the form! You cannot submit the empty form.",name=firstname)
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
    if "preferred_name" in session:
        session.pop("preferred_name",None)
    else:
        session.pop("first_name",None)

    return redirect(url_for("login"))

if __name__=="__main__":
    app.run(debug=True)