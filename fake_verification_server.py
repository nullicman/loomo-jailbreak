# experimental right now -- working on jailbreak that doesn't require flashing.
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/v1/robot/activate', methods=['POST'])
def activate():
    try:
        # Log all request details
        print("\n=== Incoming Activation Request ===")
        print(f"Headers: {dict(request.headers)}")
        print(f"Content-Type: {request.content_type}")
        print(f"Raw Data: {request.get_data(as_text=True)}")
        
        data = request.get_json()
        print(f"Parsed JSON Data: {json.dumps(data, indent=2)}")
        
        serial_number = data.get('ossn')
        sn_hash = data.get('activateKey')
        
        print(f"\nExtracted Values:")
        print(f"Serial Number (ossn): {serial_number}")
        print(f"Serial Hash (activateKey): {sn_hash}")
        
        # Create response using the received values
        response = {
            "resultCode": "9000",
            "resultDesc": "Success",
            "data": {
                "securityKey": "super_secret_key",
                "secret": "8319116100-611153335-125836820116", # from sample good Loomo
                "robotId": serial_number,  # Use the actual serial number
                "robotKey": sn_hash       # Use the SHA1 hash we received
            }
        }
        
        print("\n=== Sending Response ===")
        print(json.dumps(response, indent=2))
        print("============================\n")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"\nError processing request: {e}")
        return jsonify({
            "resultCode": "9001",
            "resultDesc": f"Error: {str(e)}"
        }), 500

@app.route('/v3/robot/getAgreement', methods=['GET'])
def get_agreement():
    try:
        # Log request details
        print("\n=== Incoming GetAgreement Request ===")
        print(f"Headers: {dict(request.headers)}")
        print(f"Args: {dict(request.args)}")
        
        # Extract values from query params
        user_id = request.args.get('userId')
        robot_id = request.args.get('robotId')
        robot_key = request.args.get('robotKey')
        
        print(f"\nExtracted Values:")
        print(f"User ID: {user_id}")
        print(f"Robot ID: {robot_id}")
        print(f"Robot Key: {robot_key}")
        
        # Create success response
        response = {
            "resultCode": "9000",
            "resultDesc": "Success",
            "data": {
                "agreementStatus": True
            }
        }
        
        print("\n=== Sending Response ===")
        print(json.dumps(response, indent=2))
        print("============================\n")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"\nError processing request: {e}")
        return jsonify({
            "resultCode": "9001",
            "resultDesc": f"Error: {str(e)}"
        }), 500

@app.route('/v3/robot/agreement', methods=['POST'])
def post_agreement():
    try:
        # Log request details
        print("\n=== Incoming Agreement POST Request ===")
        print(f"Headers: {dict(request.headers)}")
        print(f"Content-Type: {request.content_type}")
        print(f"Raw Data: {request.get_data(as_text=True)}")
        
        data = request.get_json()
        print(f"Parsed JSON Data: {json.dumps(data, indent=2)}")
        
        # Extract values
        user_id = data.get('userId')
        robot_id = data.get('robotId')
        robot_key = data.get('robotKey')
        
        print(f"\nExtracted Values:")
        print(f"User ID: {user_id}")
        print(f"Robot ID: {robot_id}")
        print(f"Robot Key: {robot_key}")
        
        # Create success response
        response = {
            "resultCode": "9000",
            "resultDesc": "Success"
        }
        
        print("\n=== Sending Response ===")
        print(json.dumps(response, indent=2))
        print("============================\n")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"\nError processing request: {e}")
        return jsonify({
            "resultCode": "9001",
            "resultDesc": f"Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)