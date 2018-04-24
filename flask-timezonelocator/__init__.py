import os
from flask import Flask, render_template, request
import json

from timezone_locator import *

app = Flask(__name__)
app.secret_key="Replace_this_with_super_secret_key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-timezone/', methods=['GET','POST'])
def timezone_api():
    try:
        coordinates = json.loads(request.data.decode('utf-8'))
        res = get_timezone(coordinates['lon'], coordinates['lat'])
        
        #TZ is found
        if res and res is not 'Undefined':
            return json.dumps({'success':True, 'result':res}), 200, {'ContentType':'application/json'}

        #TZ is not found, error message
        else:
            return json.dumps({'success':False, 'error':'Could not comply, please check your coordinates'}), 200, {'ContentType':'application/json'}
    
    except Exception as e:
        #Log error somewhere
        print(e)
        #Inform user that something went wrong
        return json.dumps({'success':False, 'error':'Something went wrong with the application'}), 200, {'ContentType':'application/json'}

@app.route('/timezones', methods=['GET','POST'])
def timezone():
    try:
        if request.args:
            coordinates = request.args
            res = get_timezone(coordinates['lon'], coordinates['lat'])
            if res and res is not 'Undefined':
                return json.dumps({'success':True, 'result':res}), 200, {'ContentType':'application/json'}
            else:
                return json.dumps({'success':False, 'error':'Could not comply, please check your coordinates'}), 200, {'ContentType':'application/json'}
        else:
            return json.dumps({'success':True, 'timezones': get_all_timezones()}), 200, {'ContentType':'application/json'}

    except Exception as e:
        print(e)
        return json.dumps({'success':False, 'error':'Something went wrong with the application'}), 200, {'ContentType':'application/json'}


if __name__ == '__main__':
    app.run()
