from flask import Flask,jsonify,request 
import os

API_KEY = os.getenv('API_KEY')
def checkAuth(request):

    if 'X-AUTH-TOKEN' in request.headers:
        if request.headers['X-AUTH-TOKEN'] == API_KEY:
            return True
        else:
            return False
    else:
        return False