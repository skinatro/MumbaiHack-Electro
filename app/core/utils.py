from flask import jsonify

def api_response(data=None, message=None, status_code=200, error=None):
    response = {
        'status': 'success' if status_code < 400 else 'error',
    }
    
    if data is not None:
        response['data'] = data
        
    if message:
        response['message'] = message
        
    if error:
        response['error'] = error
        
    return jsonify(response), status_code
