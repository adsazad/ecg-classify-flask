from flask import Flask,jsonify,request 
import os

def checkAuth(request):
    API_KEY = "c7c28624-0a98-4257-ab7b-8604325cd8ee"
    if 'X-AUTH-TOKEN' in request.headers:
        if request.headers['X-AUTH-TOKEN'] == API_KEY:
            return True
        else:
            return False
    else:
        return False