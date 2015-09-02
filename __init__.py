from flask import Flask, jsonify, make_response, redirect, request, render_template
import os
import json
import urllib
import requests
from werkzeug import secure_filename
from datetime import datetime
from creds import client_id, client_secret

app = Flask(__name__)

# Config
callback = 'http://bostonhacks.io:5000/auth/mlh/callback'
# callback = 'http://localhost:5000/auth/mlh/callback'

######################## FOLDERS / FILES DATA ########################
# UPLOAD_FOLDER = '/var/www/bostonhacks/bostonhacks/attendee_data/'
UPLOAD_FOLDER = 'attendee_data/'
app = Flask(__name__)

file_types = ['pdf', 'png', 'jpg', 'jpeg', 'gif']
ALLOWED_EXTENSIONS = set(file_types)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

user_info = {'':''}
user_email = ''
######################## FOLDERS / FILES DATA ########################

def fetch_user(access_token):
  base_url = "https://my.mlh.io/api/v1/user"
  qs = urllib.urlencode({'access_token': access_token})
  # Tokens don't expire, but users can reset them, so best to do some error
  # handling here too.
  return requests.get(base_url + '?' + qs).json()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload():
    global user_email
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            filename = os.path.join("{}/{}".format(UPLOAD_FOLDER, user_email), "%s.%s" %
                (now.strftime("%Y-%m-%d-%H-%M-%S")+"_{}_resume".format(user_email), file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            return jsonify({"success":True})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth/mlh')
def auth_with_provider():
  # Step 1: Request an Authorization Code from My MLH by directing a user to
  # your app's authorize page.

  base_url = "https://my.mlh.io/oauth/authorize"
  qs = urllib.urlencode({
    'client_id': client_id,
    'redirect_uri': callback,
    'response_type': 'code'
  })

  return redirect(base_url + '?' + qs)

@app.route('/auth/mlh/callback', methods=['GET', 'POST'])
def auth_with_provider_callback():
    global user_info
    global user_email

    # Step 2: Assuming the user clicked authorize, we should get an Authorization
    # Code which we can now exchange for an access token.

    code = request.args.get('code')
    base_url = "https://my.mlh.io/oauth/token"
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': callback
    }

    if not code:
        # If somehow we got here without a code, tell the user it's an invalid request
        return make_response('Error: No code found', 400)

    resp = requests.post(base_url, json=body)

    if resp.status_code == requests.codes.ok:
        # Step 3: Now we should have an access token which we can use to get the
        # current user's profile information.  In a production app you would
        # create a user and save it to your database at this point.

        user_info = fetch_user(resp.json()['access_token'])
        user_email = user_info['data']['email']
        dictionary = {}
        for key, value in user_info['data'].iteritems():
            if(key == "phone_number"):
                dictionary["Phone number"] = value
            if(key == "first_name"):
                dictionary["First name"] = value
            if(key == "last_name"):
                dictionary["Last name"] = value
            if(key == "dietary_restrictions"):
                dictionary["Diet restrictions"] = value
            if(key == "gender"):
                dictionary["Gender"] = value
            if(key == "graduation"):
                dictionary["Graduation"] = value
            if(key == "email"):
                dictionary["Email"] = value
            if(key == "school"):
                dictionary["School"] = value['name']
            if(key == "date_of_birth"):
                dictionary["Date of birth"] = value
            if(key == "special_needs"):
                dictionary["Special needs"] = value
            if(key == "shirt_size"):
                dictionary["Shirt size"] = value
            if(key == "major"):
                dictionary["Major"] = value
        print(user_email)
        if os.path.exists("{}/{}/user_info.txt".format(UPLOAD_FOLDER, user_email)) != True:
            if os.path.isdir("{}/{}".format(UPLOAD_FOLDER, user_email)) != True:
            	os.makedirs("{}/{}".format(UPLOAD_FOLDER, user_email))
            return render_template('post_registration.html', data=dictionary)
        else:
            return render_template('thanks.html')
    else:
        return redirect('/', code=302)

@app.route('/post_registration/thanks', methods=['GET', 'POST'])
def post_registration():
    global user_info
    global user_email
    error=None
    if request.method == 'POST':
        user_info['data']['reqReimbursements'] = request.form['reimbursements']
        if request.form['whereReimbursements'] != "":
            user_info['data']['reimbursements'] = request.form['whereReimbursements']
        user_info['data']['awesome'] = request.form['awesome']
        usr_info = json.dumps(user_info, indent=4, sort_keys=True)
        with open('{}/'.format(UPLOAD_FOLDER)+user_email+'/user_info.txt', 'a') as info:
            info.write(str(usr_info))#str(user_info))
        return render_template('thanks.html', error=error)
    else:
        return "Please upload a file of type: " + str(', '.join(file_types))
    return "incorrect request"

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Preliminary logout button in the works.
    """
    if request.method == 'POST':
        base_url = "https://my.mlh.io/logout"
        resp = requests.post(base_url)
        return redirect('/')

if __name__ == '__main__':
  app.run()
