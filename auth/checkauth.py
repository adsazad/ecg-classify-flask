from flask import Flask,jsonify,request 
import os

API_KEY = os.getenv('API_KEY')
def checkAuth(request):

    if 'x-auth-token' in request.headers:
        if request.headers['x-auth-token'] == API_KEY:
            return True
        else:
            return False
    else:
        return False