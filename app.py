from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + "eyJraWQiOiIyMDIwMTEyMTE4MzQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC01NTAwMDhISlc4IiwiaWQiOiJJQk1pZC01NTAwMDhISlc4IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMzVmMDMwOTgtMjVlMy00ZmI3LWJlNDItODQ0MGI3MGIwMmQ5IiwiaWRlbnRpZmllciI6IjU1MDAwOEhKVzgiLCJnaXZlbl9uYW1lIjoiQWJoaW5hdiIsImZhbWlseV9uYW1lIjoiS3VtYXIiLCJuYW1lIjoiQWJoaW5hdiBLdW1hciIsImVtYWlsIjoiNG5pMThpczAwNV9iQG5pZS5hYy5pbiIsInN1YiI6IjRuaTE4aXMwMDVfYkBuaWUuYWMuaW4iLCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJmZmE0OWE0NGZmNjg0MGJiOTc0YWYyMmI5NDlkMTgyYyIsImZyb3plbiI6dHJ1ZX0sImlhdCI6MTYwODE4NDkxOSwiZXhwIjoxNjA4MTg4NTE5LCJpc3MiOiJodHRwczovL2lhbS5ibHVlbWl4Lm5ldC9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.aRyTDRa4-m6jMdsStWtrOI51oVewxDAPaUDykEU6L4B75Q3eWJ5BcmKavKFKwXhySrs4XUpU1zAxTr7-l5awLMYJVoLfR2L7wC7_GlDTShEPSvoX_jUyyekMMKzAIshP_utV5LzEhJs4klzBLOfSuQTlh49PKodhGPIy8njEnLSbPu-NRwb01W-E3si2I1w3wPM_u_gUCnWPBljThaoLrLC28VqSDOFL67H2fK-lpVsKFV5j-P14g7dm2ckdxqUYFrhIgeAKdHtAuHx1njXaffo0dAZmooYaaP_6gI_Ajh1WFgegeAnfkA7kEpvYaQIQN07SEgmnMRrYVXdO_xx8rQ"}
        python_object = [float(form.Wind_Speed.data), float(form.Theoretical_Power_Curve.data), float(form.Wind_Direction.data)]
        #Transform python objects to  Json
        #print(python_object)
        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["Wind Speed (m/s)", "Theoretical_Power_Curve (KWh)", "Wind Direction (°)"], "values": userInput }]}
        #print(payload_scoring)
        response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e42cf888-7ee0-4a9c-bddc-3c4adf3fa2cb/predictions?version=2020-12-14", json=payload_scoring, headers=header)
        print(response_scoring.text)
        output = json.loads(response_scoring.text)
        #print(output)
        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]

  
        form.abc = bc[0][0] # this returns the response back to the front page
        return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
