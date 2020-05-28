from flask import Flask, render_template, Markup, request
from werkzeug.datastructures import ImmutableMultiDict
import json
import requests


app = Flask(__name__)
@app.route('/')
def first():
	title = "Welcome. Select one"
	return render_template('index.html', title=title)

@app.route('/static_routing')
def second():
	return render_template('temp.html')

@app.route('/firewall')
def third():
	return render_template('fire.html')

@app.route('/details_page', methods=['GET', 'POST'])
def fourth():
	data_config = request.form
	data = static_entries(data_config)	
	return render_template('temp1.html', data=data)

@app.route('/details_page1', methods=['GET', 'POST'])
def fifth():
	data_config = request.form
	data = firewall(data_config)	
	return render_template('fire1.html', data=data)

def static_entries(data_config):
	dict_data = data_config.to_dict(flat=True)
	if not dict_data['ipv4_dst']:
		del dict_data['ipv4_dst']
	dict_data['actions'] = "output=" + dict_data['actions']
	json_data = json.dumps(dict_data)
	cmd = requests.post('http://192.168.56.105:8080/wm/staticentrypusher/json',data=(json_data),headers={'Content-Type':'application/json'})  
	return cmd.text

def firewall(data_config):
	cmd_block = requests.post('http://192.168.56.105:8080/wm/firewall/module/enable/json')
	dict_data = data_config.to_dict(flat=True)
	print(dict_data)
	dict_data['actions'] = "output=" + dict_data['actions']
	json_data = json.dumps(dict_data)
	cmd = requests.post('http://192.168.56.105:8080/wm/staticentrypusher/json',data=(json_data),headers={'Content-Type':'application/json'})
	return cmd.text


if __name__ == '__main__':
	app.debug = True
	app.run(host = '192.168.56.105', port = 80)
