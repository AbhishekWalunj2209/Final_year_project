import pickle
import numpy as np
from flask import Flask , render_template , request ,redirect,url_for

app=Flask(__name__)
model=pickle.load(open('final_model.pkl','rb'))
#url/
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/index1')
def index1():
    return render_template('index1.html')

@app.route('/result',methods=['POST','GET'])
def result():

    Gender = request.form['Gender']
    family_history_with_overweight = request.form['family_history_with_overweight']
    FAVC = request.form['FAVC']
    CAEC = request.form['CAEC']
    SMOKE = request.form['SMOKE']
    SCC = request.form['SCC']
    CALC = request.form['CALC']
    MTRANS = request.form['MTRANS']

    # Convert the data into the sample_data format
    sample_data = {
        'Age': float(request.form['Age']),
        'FCVC': int(request.form['FCVC']),
        'NCP': int(request.form['NCP']),
        'CH2O': int(request.form['CH2O']),
        'FAF': int(request.form['FAF']),
        'TUE': int(request.form['TUE']),
        'Gender_Female': 1 if Gender == 'female' else 0,
        'Gender_Male': 1 if Gender == 'Male' else 0,
        'family_history_with_overweight_no': 1 if family_history_with_overweight == 'family_history_with_overweight_no' else 0,
        'family_history_with_overweight_yes': 1 if family_history_with_overweight == 'family_history_with_overweight_yes' else 0,
        'FAVC_no': 1 if FAVC == 'FAVC_no' else 0,
        'FAVC_yes': 1 if FAVC == 'FAVC_yes' else 0,
        'CAEC_Always': 1 if CAEC == 'CAEC_always' else 0,
        'CAEC_Frequently': 1 if CAEC == 'CAEC_frequently' else 0,
        'CAEC_Sometimes': 1 if CAEC == 'CAEC_sometimes' else 0,
        'CAEC_no': 1 if CAEC == 'CAEC_no' else 0,
        'SMOKE_no': 1 if SMOKE == 'SMOKE_no' else 0,
        'SMOKE_yes': 1 if SMOKE == 'SMOKE_yes' else 0,
        'SCC_no': 1 if SCC == 'SCC_no' else 0,
        'SCC_yes': 1 if SCC == 'SCC_yes' else 0,
        'CALC_Always': 1 if CALC == 'CALC_always' else 0,
        'CALC_Frequently': 1 if CALC == 'CALC_frequently' else 0,
        'CALC_Sometimes': 1 if CALC == 'CALC_sometimes' else 0,
        'CALC_no': 1 if CALC == 'CALC_no' else 0,
        'MTRANS_Automobile': 1 if MTRANS == '1' else 0,
        'MTRANS_Bike': 1 if MTRANS == '3' else 0,
        'MTRANS_Motorbike': 1 if MTRANS == '2' else 0,
        'MTRANS_Public_Transportation': 1 if MTRANS == '4' else 0,
        'MTRANS_Walking': 1 if MTRANS == '5' else 0
    }
        
    print("Hello")
    print(sample_data)
    prediction = model.predict([list(sample_data.values())])
    print(prediction)
    result=''
    if prediction==0:
        result='Not Obese'
    else:
        result="Obese"

    prediction=''
    obese=''
    Bonus=''
    if result=='Obese':
        obese='No need to worry!'
        if sample_data['FAVC_yes']==1 and sample_data['FAF']<=1:
            prediction+=" Reduce your calorie intake and should exercise at least for 1.5 hours. \n"
        if sample_data['CALC_Frequently']==1 or sample_data['CALC_Always']==1:
            prediction+=" Reduce your alcohol intake it will be great for your health. \n"
        if sample_data['SMOKE_yes']==1:
            prediction+=" Smoking is not good for your health. \n"
        if sample_data['MTRANS_Walking']!=1:
            prediction+=" At least walk for 2 kms daily. \n"
        if sample_data['CH2O']==1:
            prediction+=" Drink more water, It will keep you hydrated and fresh. \n"
        if sample_data['NCP']>2:
            prediction+=" Limit your number of meals. \n"
        if sample_data['CAEC_Always']==1 or sample_data['CAEC_Frequently']==1:
            prediction+=" Avoid junk food as possible. \n"
        Bonus="BONUS TIP : Follow a diet plan & include green vegetables in your diet. "

    else:
        obese='Great!!!, just keep going on your routine'
        if sample_data['CALC_Frequently']==1 or sample_data['CALC_Always']==1:
            prediction+=" Reduce your alcohol intake it will be great for your health. \n"
        if sample_data['SMOKE_yes']==1:
            prediction+=" Smoking is not good for your health. \n"
        if sample_data['MTRANS_Walking']!=1:
            prediction+=" At least walk for 2 kms daily. \n"
        if sample_data['CH2O']==1:
            prediction+=" Drink more water, It will keep you hydrated and fresh. \n"
        if sample_data['CAEC_Always']==1 or sample_data['CAEC_Frequently']==1:
            prediction+=" Avoid junk food as possible. \n"
        Bonus="BONUS TIP : Include green vegetables in your diet and as much as water."

        print(prediction)

    return render_template('result.html',predct=result,obese=obese,prediction=prediction,bonus=Bonus)


if __name__=='__main__':
    app.run(debug=True)


