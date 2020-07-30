from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
import pickle
import numpy as np
app = Flask(__name__)
model = pickle.load(open('finalized_model.pickle', 'rb'))


@app.route('/',methods=['GET','POST'])
@cross_origin()
def Home():
    return render_template('index.html')

@app.route("/work", methods=['GET','POST'])
@cross_origin()
def predict():
    if request.method == 'POST':
        year_old = int(request.form['Year'])
        present_price = float(request.form['Present_Price'])
        kms_driven = int(request.form['Kms_Driven'])
        kms_driven = np.log(kms_driven)
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if (Fuel_Type_Petrol == 'Petrol'):
            fuel_type_Petrol = 1
            fuel_type_Diesel = 0
        else:
            fuel_type_Petrol = 0
            fuel_type_Diesel = 1
        year_old = 2020 - year_old
        seller_type_Individual = request.form['Seller_Type_Individual']
        if (seller_type_Individual == 'Individual'):
            seller_type_Individual = 1
        else:
            seller_type_Individual = 0
        transmission_Manual = request.form['Transmission_Mannual']
        if (transmission_Manual == 'Mannual'):
            transmission_Manual = 1
        else:
            transmission_Manual = 0
        prediction = model.predict([[present_price,kms_driven,year_old,fuel_type_Diesel,fuel_type_Petrol,seller_type_Individual,transmission_Manual]])
        output = round(prediction[0],2)
        if(output<0):
            return render_template('index.html',prediction_text="oh sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="Selling price of the car  : {} lakhs ".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)