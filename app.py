# coding=utf-8

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired
import sys
sys.path.append('/Users/egecamlibel/Desktop/iyzicoSubscriptionProject/iyzipay-python-master')
import iyzipay
import json
import requests
import pdb


options12 = {
  'api_key' : 'sandbox-U24kOS7fdIrzJkgB8e3NZTkAFIXAjmIL',
  'secret_key' : 'sandbox-qtQ4H120ik7TbcOogvqQDXfgyCEPxf9Q',
  'base_url': "sandbox-api.iyzipay.com"
}
payment_card = {
    'cardHolderName': 'John Doe',
    'cardNumber': '5528790000000008',
    'expireMonth': '12',
    'expireYear': '2030',
    'cvc': '123',
    'registerCard': '0',
    'registerConsumerCard': False
}

#PRODUCT 1 AND 2 CREATION

# requestProduct1= {
#     'locale': 'tr',
#     'conversationId': 1234,
#     'name': 'Kutu 1',
#     'description': 'Haftalik Plan, 6 ay boyunca her hafta kitap yolluyoruz!'
# }
# reportProduct1 = iyzipay.SubscriptionProduct().create(requestProduct1, options)
# print(reportProduct1.read().decode('utf-8'))

# requestProduct2= {
#     'locale': 'tr',
#     'conversationId': 1234,
#     'name': 'Kutu 2',
#     'description': 'Aylik Plan, 12 ay boyunca her ay kitap yolluyoruz!'
# }
# reportProduct2 = iyzipay.SubscriptionProduct().create(requestProduct2, options)
# print(reportProduct2.read().decode('utf-8'))

# PRICINGPLANLARI OLUSTURMA VE PRODUCTLARA REFER ETME

# requestAylikPlan = {
#     'locale': 'tr',
#     'conversationId': 1234,
#     'name': 'Haftalik Plan',
#     'price': 19.90,
#     'currencyCode': 'TRY',
#     'paymentInterval': 'WEEKLY',
#     'paymentIntervalCount': 1,
#     'planPaymentType': 'RECURRING',
#     'recurrenceCount': 6,
#     'referenceCode': 'f443917a-f789-45ec-8ca2-7450c71b111a'
# }
#
# reportAylikPlan = iyzipay.SubscriptionPlan().create(requestAylikPlan, options)
# print(reportAylikPlan.read().decode('utf-8'))

# requestAylikPlan = {
#     'locale': 'tr',
#     'conversationId': 1234,
#     'name': 'Aylik Plan',
#     'price': 49.90,
#     'currencyCode': 'TRY',
#     'paymentInterval': 'MONTHLY',
#     'paymentIntervalCount': 1,
#     'planPaymentType': 'RECURRING',
#     'recurrenceCount': 12,
#     'referenceCode': 'e00cbcf4-3c41-4677-aad2-f7508ed5add2'
# }
#
# reportAylikPlan = iyzipay.SubscriptionPlan().create(requestAylikPlan, options)
# print(reportAylikPlan.read().decode('utf-8'))

product1referenceCode = 'f443917a-f789-45ec-8ca2-7450c71b111a'
product2referenceCode = "e00cbcf4-3c41-4677-aad2-f7508ed5add2"

product1paymentplancode = "c00708fa-ca5b-4e13-bb57-deffc5517f7c"
product2paymentplancode = "501f3ecd-b403-4d0f-8b49-a4d758253001"

# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
class InfoForm(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    ad = StringField('Ad',validators=[DataRequired()])
    soyad  = StringField("Soyad")
    email = StringField('Email',validators=[DataRequired()])
    telefonNo = StringField('Telefon No')
    tcKimlikNo = StringField('TC Kimlik No')
    adres = StringField('Adres')
    sehir = StringField('Sehir')
    ulke = StringField('Ulke')
    postaKodu = StringField('Posta Kodu')
    product = SelectField(u'Abonelik Turu', choices=[("501f3ecd-b403-4d0f-8b49-a4d758253001", '12 Aylik Abonelik, Her ay kitap, 49.90'),("c00708fa-ca5b-4e13-bb57-deffc5517f7c",'6 Aylik Abonelik, Her hafta kitap, 19.90')])
    submit = SubmitField('Submit')



app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!

app.config['SECRET_KEY'] = 'mysecretkey'
@app.route('/', methods=['GET', 'POST'])

def index():
    # Create instance of the form.
    form = InfoForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        # Grab the data from the breed on the form.

        session['ad'] = form.ad.data
        session['soyad'] = form.soyad.data
        session['email'] = form.email.data
        session['telefonNo'] = form.telefonNo.data
        session['tcKimlikNo'] = form.tcKimlikNo.data
        session['adres'] = form.adres.data
        session['sehir'] = form.sehir.data
        session['ulke'] = form.ulke.data
        session['postaKodu'] = form.postaKodu.data
        session['product'] = form.product.data
        address = {
            'contactName': form.ad.data + "" + form.soyad.data,
            'city': form.sehir.data,
            'country': form.ulke.data,
            'address': form.adres.data,
            'zipCode': form.postaKodu.data
        }

        requestToPersonCreate = {
            'locale': 'tr',
            'conversationId': '8138',
            'name': form.ad.data,
            'surname': form.soyad.data,
            'email': form.email.data,
            'gsmNumber': form.telefonNo.data,
            'identityNumber': form.tcKimlikNo.data,
            'billingAddress': address,
            'shippingAddress': address
        }

        report2 = iyzipay.SubscriptionCustomer().create(requestToPersonCreate, options12)


        if (form.product.data) == "c00708fa-ca5b-4e13-bb57-deffc5517f7c":
            session['urunadi'] = 'Haftalik Plan'
            pricingPlanReferenceCode = "c00708fa-ca5b-4e13-bb57-deffc5517f7c"
        else:
            session['urunadi'] = 'Aylik Plan'
            pricingPlanReferenceCode = "501f3ecd-b403-4d0f-8b49-a4d758253001"


        request1 = {
            'locale': 'tr',
            'conversationId': 'e234324324',
            'pricingPlanReferenceCode': pricingPlanReferenceCode,
            'customer': requestToPersonCreate,
            'paymentCard': payment_card,
            'shippingAddress': address,
            'billingAddress': address,
        }


        finalreport = iyzipay.SubscriptionCheckoutDirect().create(request1, options12)

        session['report'] = finalreport.read().decode('utf-8')
        print(session['report'][12])
        if(session['report'][11] == "s"):
            return redirect(url_for('thankyou'))
        else:
            return redirect(url_for('failed'))


    return render_template('index.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/failed')
def failed():
    return render_template('failed.html')


if __name__ == '__main__':
    app.run(debug=True)
