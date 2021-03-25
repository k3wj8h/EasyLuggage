import flask
from flask import render_template, request, jsonify, g, redirect, url_for
import sqlite3
import json
import requests


"""
Sources:
https://flask.palletsprojects.com/en/1.1.x/quickstart/
#https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
"""

"""
TODO
- Long polling: https://github.com/sigilioso/long_polling_example
- HTML templates
"""

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app_host = "localhost"
app_port = 5000
base_url = "http://" + app_host + ":" + str(app_port)


@app.route('/', methods=['GET'])
def home():
    url = base_url + "/luggages"
    data = json.loads(requests.get(url).text)
    return render_template('index_tmpl.html', data=data)


@app.route('/new_luggage', methods=['POST'])
def new_luggage():
    if request.method == "POST":
        url = base_url + "/luggages"
        headers = {"Content-Type": "application/vnd.api+json"}
        data = {"data": {"type": "luggage", "attributes": {"name": request.form['name'], "address": request.form['address']}}}
        requests.post(url, headers=headers, data=json.dumps(data))
    return redirect(url_for('home'))


@app.route('/luggages/<int:luggages_id>', methods=['GET', 'POST'])
def luggage(luggages_id=None):
    if request.method == "POST":
        url = base_url + "/luggages/" + str(luggages_id)
        headers = {"Content-Type": "application/vnd.api+json"}
        requests.delete(url, headers=headers)
        return redirect(url_for('home'))
    else:
        url = base_url + "/boxes?filter=[{\"name\":\"luggage_id\",\"op\":\"eq\",\"val\":" + str(luggages_id) + "}]"
        boxes_data = json.loads(requests.get(url).text)
        url = base_url + "/luggages/" + str(luggages_id)
        luggage_data = json.loads(requests.get(url).text)
        return render_template('luggage_tmpl.html', luggage_data=luggage_data, boxes_data=boxes_data)


@app.route('/luggages/<int:luggages_id>/new_box', methods=['POST'])
def new_box(luggages_id=None):
    if request.method == "POST":
        url = base_url + "/boxes"
        headers = {"Content-Type": "application/vnd.api+json"}
        data = {"data": {"type": "box", "attributes": {"luggage_id": luggages_id, "size": request.form['size'], "isOpen": 0}}}
        requests.post(url, headers=headers, data=json.dumps(data))
    return redirect(url_for('luggage', luggages_id=luggages_id))


@app.route('/luggages/<int:luggages_id>/boxes/<int:boxes_id>', methods=['GET'])
def box(luggages_id=None, boxes_id=None):
    if request.method == "GET":
        url = base_url + "/luggages/" + str(luggages_id)
        luggage_data = json.loads(requests.get(url).text)
        url = base_url + "/boxes/" + str(boxes_id)
        box_data = json.loads(requests.get(url).text)
    return render_template('box_tmpl.html', luggage_data=luggage_data, box_data=box_data)


@app.route('/luggages/<int:luggages_id>/boxes/<int:boxes_id>/open', methods=['POST'])
def box_open(luggages_id=None, boxes_id=None):
    if request.method == "POST":
        url = base_url + "/boxes/" + str(boxes_id)
        headers = {"Content-Type": "application/vnd.api+json"}
        data = {"data": {"type": "box", "id": boxes_id, "attributes": {"isOpen": 1}}}
        requests.patch(url, headers=headers, data=json.dumps(data))
    return redirect(url_for('luggage', luggages_id=luggages_id))


@app.route('/luggages/<int:luggages_id>/boxes/<int:boxes_id>/close', methods=['POST'])
def box_close(luggages_id=None, boxes_id=None):
    if request.method == "POST":
        url = base_url + "/boxes/" + str(boxes_id)
        headers = {"Content-Type": "application/vnd.api+json"}
        data = {"data": {"type": "box", "id": boxes_id, "attributes": {"isOpen": 0}}}
        requests.patch(url, headers=headers, data=json.dumps(data))
    return redirect(url_for('luggage', luggages_id=luggages_id))


@app.route('/luggages/<int:luggages_id>/delete_box/<int:boxes_id>', methods=['POST'])
def delete_box(luggages_id=None, boxes_id=None):
    if request.method == "POST":
        url = base_url + "/boxes/" + str(boxes_id)
        headers = {"Content-Type": "application/vnd.api+json"}
        requests.delete(url, headers=headers)
        return redirect(url_for('luggage', luggages_id=luggages_id))

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    app.run()




