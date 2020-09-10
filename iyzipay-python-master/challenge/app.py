from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

options = {
  'api_key': "sandbox-U24kOS7fdIrzJkgB8e3NZTkAFIXAjmIL",
  'secret_key': "sandbox-qtQ4H120ik7TbcOogvqQDXfgyCEPxf9Q",
  'base_url': "sandbox-api.iyzipay.com"
}

payment_card = {
    'cardHolderName': 'John Doe',
    'cardNumber': '5528790000000008',
    'expireMonth': '12',
    'expireYear': '2030',
    'cvc': '123',
    'registerCard': '0'
}

buyer = {
    'id': 'BY789',
    'name': 'John',
    'surname': 'Doe',
    'gsmNumber': '+905350000000',
    'email': 'email@email.com',
    'identityNumber': '74300864791',
    'lastLoginDate': '2015-10-05 12:43:35',
    'registrationDate': '2013-04-21 15:12:09',
    'registrationAddress': 'Nidakule Gztepe, Merdivenky Mah. Bora Sok. No:1',
    'ip': '85.34.78.112',
    'city': 'Istanbul',
    'country': 'Turkey',
    'zipCode': '34732'
}

address = {
    'contactName': 'Jane Doe',
    'city': 'Istanbul',
    'country': 'Turkey',
    'address': 'Nidakule Gztepe, Merdivenky Mah. Bora Sok. No:1',
    'zipCode': '34732'
}

basket_items = [
    {
        'id': 'BI101',
        'name': 'Binocular',
        'category1': 'Collectibles',
        'category2': 'Accessories',
        'itemType': 'PHYSICAL',
        'price': '19.90',
        'pricingPlans':[
        {
            "productReferenceCode":"BI101",
            "name": "WEEKLYFOR6MONTHS",
            "price": "19.90"

        }]
    },
    {
        'id': 'BI102',
        'name': 'Game code',
        'category1': 'Game',
        'category2': 'Online Game Items',
        'itemType': 'VIRTUAL',
        'price': '0.5'
    },
    {
        'id': 'BI103',
        'name': 'Usb',
        'category1': 'Electronics',
        'category2': 'Usb / Cable',
        'itemType': 'PHYSICAL',
        'price': '0.2'
    }
]

request = {
    'locale': 'tr',
    'conversationId': '123456789',
    'price': '20.6',
    'paidPrice': '21',
    'currency': 'TRY',
    'paymentGroup': 'SUBSCRIPTION',
    'installment': '1',
    'basketId': 'B67832',
    'paymentChannel': 'WEB',
    'paymentGroup': 'PRODUCT',
    'paymentCard': payment_card,
    'buyer': buyer,
    'shippingAddress': address,
    'billingAddress': address,
    'basketItems': basket_items
}

payment = iyzipay.Subscription().create(request, options)

print(payment.read().decode('utf-8'))


