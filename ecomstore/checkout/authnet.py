'''
Created on Feb 6, 2016

@author: wale
'''

import http.client
import urllib

from ecomstore import settings


def do_auth_capture(amount='0.00', card_num=None, exp_date=None,card_cvv=None):

    delimiter = '|'
    raw_params = {
                  'x_login':settings.AUTHNET_LOGIN,
                  'x_tran_key':settings.AUTHNET_KEY,
                  'x_type':'AUTH_CAPTURE',
                  'x_amount':amount,
                  'x_version':'3.1',
                  'x_card_num':card_num,
                  'x_exp_date':exp_date,
                  'x_delim_char':delimiter,
                  'x_relay_response':'FALSE',
                  'x_delim_data':'TRUE',
                  'x_card_code':card_cvv
                }
    params = urllib.parse.urlencode(raw_params)
    headers = { 'content-type':'application/x-www-form-urlencoded',
    'content-length':len(params) }
    post_url = settings.AUTHNET_POST_URL
    post_path = settings.AUTHNET_POST_PATH
    cn = http.client.HTTPSConnection(post_url,http.client.HTTPS_PORT)
    cn.request('POST',post_path,params,headers)
    return cn.getresponse().read().decode('UTF-8').split(delimiter)
#     cn=httplib2.Http()
#     content,response=cn.request("http://test.authorize.net/gateway/transact.dll", method="POST", body=params)
#     return response.read().split(delimiter)