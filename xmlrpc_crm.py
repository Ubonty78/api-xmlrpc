#import client
import falcon
import json
from xmlrpc import client
import psycopg2
import psycopg2.extras
from pgcrm import connectpg

# stream = req.stream.read().decode('UTF-8') # Get x-www-form-urlencoded
# #context = req.context['request'] Fail
# media = req.media

# getparam = req.get_param('emailaddress3')
# bounded_stream = req.bounded_stream.read().decode('UTF-8') # Get form-data

class CreateLead():

    def on_post(self, req, resp ):
        param_as_list = req.get_param_as_list('token_key')
        print(param_as_list)
        raw_json = req.bounded_stream.read().decode('UTF-8')

        # Objson = {
        # 'timeframe':'4-6 Months',
        # 'channel_id':1546,
        # 'branch':'P3S',
        # 'mobilephone':'0924798585',
        # 'carmodel':'All+New+Honda+CIVIC',
        # 'utm_source':'google',
        # 'emailaddress1':'napatsakamol4798585@gmail.com',
        # 'firstname':'Chujai DangDoi',
        # 'mit_lineid':'timnapatkamon'
        # # }
        # print(type(Objson))   # variable dict

        objson = json.loads(raw_json)
        print(type(objson))     #  dict
        print(objson['branch'])  # for access

        print(type(req.bounded_stream.read()))  #b Byte
        print(type(raw_json))    # string

        username='admin'
        pwd='ramathree'
        dbname='h3crm_2019_test'

        url="http://192.168.82.220:8069/xmlrpc/common"
        sock = client.ServerProxy(url)
        uid = sock.login(dbname, username, pwd)
        url = "http://192.168.82.220:8069/xmlrpc/object"
        sock = client.ServerProxy(url)

        # Fix Queue
        fix_queue_id = 1

        assignto = sock.execute(dbname, uid, 'ramathree', 'crm.queue.master','func_get_queue', [])	

	    # # Management and fequency assign lead
        # assignto = {
        #     'company_id' : rp_com_id,
        #     'section_id' : rp_sec_id,
        #     'sale_id' : currentsaleid,
        # }

        description = """ Email : %s ,\n Mobile: %s ,\n TimeFrame : %s ,\n Source : %s 
        """ % (objson['emailaddress1'],objson['mobilephone'],objson['timeframe'],objson['utm_source'])
        # New Customer
        new_customer = {
            'name':objson['firstname'],
            'email':objson['emailaddress1'],
            'phone':objson['mobilephone'],
            'mobile':objson['mobilephone'],
            'customer':1,
            'company_id': assignto['company_id'],
            'section_id': assignto['section_id'] , 
            'user_id': assignto['sale_id'], 
            }
        ## Create New Customer
        partner_id = sock.execute(dbname, uid, 'ramathree', 'res.partner','create', new_customer)

        # New Lead
        new_data = {
            'social_line': objson['mit_lineid'],
            'name': objson['carmodel'],
            'description': description,
            'partner_name': objson['firstname'], 
            'contact_name': objson['firstname'],
            'email': objson['emailaddress1'], 
            'phone': objson['mobilephone'], 
            'mobile':objson['mobilephone'],
            'company_id': assignto['company_id'],
            'section_id': assignto['section_id'] , 
            'user_id': assignto['sale_id'], 
            'stage_id': 1, 
            'partner_id': partner_id,
            'type':'lead',
            'group_channel_id': 1,
            'channel_id': 67,
        }
        # Create New lead
        lead_id = sock.execute(dbname, uid, 'ramathree', 'crm.lead','create', new_data)

        resp.body = raw_json
        resp.status = falcon.HTTP_200

class SearchLead():

    def on_get(self, req, resp , saleid):
        
        print(""" Get date from %s """ % (mobile) )
	
        username='admin'
        pwd='ramathree'
        dbname='h3crm_2019_test'

        url="http://192.168.82.220:8069/xmlrpc/common"
        sock = client.ServerProxy(url)
        uid = sock.login(dbname, username, pwd)
        url = "http://192.168.82.220:8069/xmlrpc/object"
        sock = client.ServerProxy(url)

        raw_json = req.bounded_stream.read().decode('UTF-8')
        resp.body = saleid
        resp.status = falcon.HTTP_200
