from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains on all routes. For production, you might want to restrict this.
# CORS(app, resources={r"/api/*": {"origins": "https://james-resume-5afqr6ijoq-uc.a.run.app/resume"}})
# CORS(app, supports_credentials=True, origins=["https://james-resume-5afqr6ijoq-uc.a.run.app"], methods=["POST"])


@app.route('/api/validate-token', methods=['POST'])
def validate_token():
    # Extract the token from the request body
    request_data = request.get_json()
    token = request_data.get('token')

    # Use Google's tokeninfo endpoint to validate the token
    validation_response = requests.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={token}')

    if validation_response.status_code == 200:
        # Token is valid
        token_info = validation_response.json()
        # You can add additional checks here based on the token_info contents
        # For example, check the 'aud' field to ensure it matches your client ID
        return jsonify({'valid': True, 'token_info': token_info}), 200
    else:
        # Token is invalid or expired
        return jsonify({'valid': False, 'error': 'Invalid or expired token'}), 400


if __name__ == '__main__':
    app.run(debug=True)
