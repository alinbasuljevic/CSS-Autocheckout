import requests, json, time, threading
from threading import Thread
from bs4 import BeautifulSoup as bs


def AutoCheckout():
    s = requests.Session()
    post_url = 'https://shop.ccs.com/checkout/cart/addAjax/'
    headers = {
        'DNT': '1',
        'Host': 'shop.ccs.com',
        'Origin': 'https://shop.ccs.com',
        'Referer': 'https://shop.ccs.com/converse-one-star-academy-hi-shoes-white-12-0',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'X-Prototype-Version': '1.7',
        'X-Requested-With': 'XMLHttpRequest'
        }
    payload = {
        'product': '457687',
        'related_product':'',
        'super_attribute[554]':'4979',
        
        'super_attribute[454]': '4765',
        'qty': '1'
        }

    atc_request = s.post(post_url, data=payload, headers=headers)
    json_format = json.loads(atc_request.text)
    if json_format['show_cart'] == True:
        print ('Added to Cart!')
    else:
        print ('Error')
    checkout_beginning_url = 'https://shop.ccs.com/checkout/onepage/'
    checkout_start_request = s.get(checkout_beginning_url, headers=headers)
    guest_checkout_url = 'https://shop.ccs.com/checkout/onepage/saveMethod/'
    checkout_method = {
        'method':'guest'
        }
    headers.update({'Referer': 'https://shop.ccs.com/checkout/onepage/'})
    guest_checkout_request = s.post(guest_checkout_url, data=checkout_method, headers=headers)
    print ('Starting Guest Checkout...')
    shipping_url = 'https://shop.ccs.com/checkout/onepage/saveShipping/'
    shipping_payload = {
        'shipping[address_id]': '11243691',
        'shipping[country_id]': 'US',
        'shipping[firstname]': 'Alin',
        'shipping[lastname]': 'Basuljevic',
        'shipping[street][]': '1 Test Avenue',
        'shipping[street][]': '1 Test Avenue',
        'shipping[city]': 'Manhattan',
        'shipping[region_id]': '43',
        'shipping[region]': '',
        'shipping[postcode]': '10029',
        'shipping[save_in_address_book]': '1',
        'shipping[use_for_billing]': '1',
        'shipping[telephone]': '9148110009',
        'shipping[email]': 'random@gmail.com',
        'subscribe': 'on',
        'shipping[same_as_billing]': '0'
        }
    request = s.post(shipping_url, data=shipping_payload, headers=headers)
    if request.status_code == 200:
        print ('Saved Shipping Settings, Moving to Billing Section...')
    s.post('https://shop.ccs.com/checkout/onepage/getAdditional/', headers=headers)
    s.get('https://shop.ccs.com/checkout/onepage/progress/', headers=headers)
    shipping_selection = {
        'shipping_method': 'freeshipping_freeshipping',
        'form_key': '80Bf98nGdCqfSGFM'
        }
    further_shipping = s.post('https://shop.ccs.com/checkout/onepage/saveShippingMethod/', data=shipping_selection, headers=headers)
    billing_url = 'https://shop.ccs.com/checkout/onepage/saveBilling/'
    billing_info = {
        'billing[address_id]': '11243690',
        'billing[country_id]': 'US',
        'billing[firstname]': 'Alin',
        'billing[lastname]': 'Basuljevic',
        'billing[street][]': '1 Test Avenue',
        'billing[street][]': '1 Test Avenue',
        'billing[city]': 'Manhattan',
        'billing[region_id]': '43',
        'billing[region]':'', 
        'billing[postcode]': '10541',
        'billing[save_in_address_book]': '1',
        'billing[email]': 'random@gmail.com',
        'billing[telephone]': '9148110009',
        'payment[method]': 'cybersource_soap',
        'payment[cc_type]': 'VI',
        'payment[cc_number]': '1234123412341234',
        'payment[cc_exp_month]': '3',
        'payment[cc_exp_year]': '2024',
        'payment[cc_cid]': '439',
        'coupon_code':'', 
        'remove': '0',
        'giftcard_code':''
        }
    billing_saved = s.post(billing_url, data=billing_info, headers=headers)
    if billing_saved.status_code == 200:
        print ('Successfully Saved Billing Info!')
    order_submission_url = 'https://shop.ccs.com/checkout/onepage/saveOrder/'
    order_review = {
        'payment[method]': 'cybersource_soap',
        'payment[cc_type]': 'VI',
        'payment[cc_number]': '1234123412341234',
        'payment[cc_exp_month]': '3',
        'payment[cc_exp_year]': '2024',
        'payment[cc_cid]': '439'
        }
    print ('Submitting Order...')
    order_submission = s.post(order_submission_url, data=order_review, headers=headers)
    if 'declined' in order_submission.text:
        print ('Checkout Result: Card Declined')
    else:
        print ('Checkout Result: Order Placed.')
        print (order_submission.text)

number_of_tasks = int(input('Enter Number of Threads: '))
for i in range(number_of_tasks):
    bot = threading.Thread(target=AutoCheckout())
    bot.start()
    
    
    



