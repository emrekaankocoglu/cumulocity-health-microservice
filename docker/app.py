from flask import Flask, jsonify,request,abort
from service import *
app=Flask(__name__)
@app.route('/health')
def health():
    return jsonify(status="UP")

@app.route('/deviceHealth')
def sendDeviceHealth():
    authHeader={"Authorization":""}
    authHeader["Authorization"]=request.headers.get('Authorization')
    authStatus=authenticateUser(authHeader,"ROLE_HEALTH_READ")
    if (authStatus):
        deviceId=request.args.get("source", default="", type=str)
        if(deviceId!=""):
            return jsonify(health=deviceHealth(deviceId),id=deviceId)
        else:
            abort(400)
    else:
        abort(401)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
