import os
from flask import Flask, render_template, request, send_file
import stripe
import h5py
import time
import datetime

id = 0
file = h5py.File('donations.h5', 'a')
stripe_keys = {
    'secret_key': "sk_test_HFXxSC2EHvmEa3dwQ0vz9CDL",
    'publishable_key': "pk_test_T6pOdo6D6N5YROCJUPfieSid"
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bootstrapmincss')
def bootstrapmin():
    return send_file('templates/css/bootstrap.min.css', mimetype='text/css')

@app.route('/heroicfeaturescss')
def heroicfeatures():
    return send_file('templates/css/heroic-features.css', mimetype='text/css')

@app.route('/donateashramjpg')
def donateashram():
    return send_file('templates/images/Donate_ashram.jpg')

@app.route('/donatelocaljpg')
def donatelocal():
    return send_file('templates/images/Donate_local.jpg')

@app.route('/donatecfcjpg')
def donatecfc():
    return send_file('templates/images/Donate_CFC.jpg')

@app.route('/donateeventjpg')
def donateevent():
    return send_file('templates/images/Donate_event.jpg')

@app.route('/jqueryjs')
def jqueryjs():
    return send_file('templates/js/jquery.js')

@app.route('/bootstrapminjs')
def bootstrapminjs():
    return send_file('templates/js/bootstrap.min.js')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/charge', methods=['POST'])
def charge():
    print(request.form['full_name'])
    print(request.form['amount'])
    print(request.form['zip'])
    print(request.form['province'])
    print(request.form['country'])
    amount = request.form['amount']
    millis = int(round(time.time()*1000))
    date_today = datetime.datetime.today().strftime('%Y%m%d')
    f = h5py.File('test2.hdf5', 'a')
    x = '/customers' in f
    if(x==0):
    	root = f.create_group('customers')
    else:
    	print('customers exist already')
    	root = f['/customers']
    y = '/customers/' + date_today in f
    if(y==0):
    	batch_today = root.create_group(date_today)
    else:
    	print('todays batch exists already')
    	batch_today = f['/customers/' + date_today]
    #current_customer = batch_today.create_group(str(millis))
    batch_today.create_dataset(str(millis) + '/name', data=request.form['full_name'])
    batch_today.create_dataset(str(millis) + '/email', data=request.form['email'])
    batch_today.create_dataset(str(millis) + '/street1', data=request.form['street1'])
    batch_today.create_dataset(str(millis) + '/street2', data=request.form['street2'])
    batch_today.create_dataset(str(millis) + '/city', data=request.form['city'])
    batch_today.create_dataset(str(millis) + '/province', data=request.form['province'])
    batch_today.create_dataset(str(millis) + '/zip', data=request.form['zip'])
    batch_today.create_dataset(str(millis) + '/country', data=request.form['country'])
    batch_today.create_dataset(str(millis) + '/amount', data=request.form['amount'])
    batch_today.create_dataset(str(millis) + '/stripeToken', data=request.form['stripeToken'])
       #file[datetime.datetime.today().strftime('%Y%m%d') + '/' + str(id) + '/status'] = 'pending'
    amount = int(request.form['amount'])
    print('amount is' + str(amount))
    customer = stripe.Customer.create(email=request.form['email'],card=request.form['stripeToken'])
    #current_customer['/id'] = customer.id
    print("created the customer")
    print(customer.__dict__)
    charge = stripe.Charge.create(customer=customer.id,amount=amount,currency='cad',description='Flask Charge')
    print("created the charge")
    batch_today.create_dataset(str(millis) + '/status', data='success')
    print(charge.__dict__)
    f.close()
    #file[datetime.datetime.today().strftime('%Y%m%d') + '/' + str(id) + '/status'] = 'completed'
    return render_template('charge.html',amount='$' + str(amount/100))

if __name__ == '__main__':
    app.run(debug=True)
