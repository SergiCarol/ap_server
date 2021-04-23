from flask import Flask, render_template, redirect, url_for, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import os

app = Flask(__name__)

class WifiSettings(Form):
    SSID = StringField('SSID', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@app.route('/', methods=['GET', 'POST'])
def main():
    form = WifiSettings(request.form)
    if request.method == 'POST' and form.validate():
        connectToNetwork(request)
        return redirect(url_for('done'))

    return render_template('settings.html', form=form)

@app.route('/done')
def done():
    return render_template('done.html')

def connectToNetwork(data):
    SSID = data.form['SSID']
    password = data.form['password']

    print(SSID, password)

    config_lines = [
    '\n',
    'network={',
    '\tssid="{}"'.format(SSID),
    '\tpsk="{}"'.format(password),
    '\tkey_mgmt=WPA-PSK',
    '}'
    ]
    config = '\n'.join(config_lines)
    print(config)

    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as wifi:
        wifi.write(config)

    print("Wifi config added")
    print("Restarting network to try to connect to new wifi")
    os.system("systemctl restart networking.service")