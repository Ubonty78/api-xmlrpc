import falcon
import xmlrpc
from xmlrpc_crm import SearchLead,CreateLead

class MainPage:

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.body = "Main Page"

api = falcon.API()
# =====================================
# Default 
# api.add_route('/quote', QuoteResource())
# =====================================
api.add_route('/', MainPage())
api.add_route('/cl_search/{saleid}/', SearchLead())
api.add_route('/cl_add', CreateLead())