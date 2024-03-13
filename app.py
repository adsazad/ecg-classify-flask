from flask import Flask,jsonify,request 
from auth.checkauth import checkAuth
app = Flask(__name__)
app.debug = True


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "No Route Exist"}), 404

# Define a route that triggers a 404 error
# @app.route('/404', methods=['GET'])
# def not_found_route():
#     # Simulate a situation where the route does not exist
#     return 'This route does not exist!', 404

@app.route("/classify/ecg",method=['POST'])
def predict_api():
     # check authentication
    
    user = checkAuth(request)
    if not (user):
      return jsonify({"error": "Invalid auth token"})
    ecg = request.args.get('ecg')
    if not ecg:
      return jsonify({"error": "Missing 'ecg' parameter"})
    return jsonify({"ecg": ecg})
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5002)

   

    


