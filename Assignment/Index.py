from flask import Flask, request, render_template, redirect, jsonify, url_for
import flask_login
from flask_cors import CORS
import sqlite3
import requests
import hashlib
import DataBase as db

app = Flask(__name__)
app.secret_key = b'xz\xf6\x98\x19\x1b?%\x90\x14\t\xcba"\xb8\x827\x84/N8b\xff\xf0k\x14\xd3P\xe7\xd8\xfd{\xb9\x86\xa5'  
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_SUPPORTS_CREDENTIALS"]=True

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
user_db_data = {}


def validate_user_emailid(emailId):
	connection_state = sqlite3.connect("RestaurantReview.db")
	cursor = connection_state.cursor()
	cursor.execute("SELECT emailId, password, firstname from User WHERE emailId = ?",(emailId,))
	user = cursor.fetchone()
	connection_state.close()
	if user == None:
		return 1
	user_db_data[user[0]] = {"password":user[1], "firstname":user[2]}
	return 0

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in user_db_data:
        return

    user = User()
    user.id = email
    user.name = user_db_data[email]["firstname"]
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in user_db_data:
        return
    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == user_db_data[email]['password']
    return user

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect("homepage")

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect("homepage")

@app.route('/login_error')
def login_error():
	error = ["Invalid Credentials"]
	return render_template("Login.html", error = error)


# Function which redirects to Homepage
@app.route("/homepage")
def homepage():
	return render_template("HomePage.html")


# Redirects to the Singup page
@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
	if request.method == 'GET':
		return render_template("Signup.html")

# Called from jquery to validate the user name
@app.route("/user_signup", methods = ["POST"])
def user_signup():
	if request.method == "POST":
		user_response = request.get_json()
		if validate_user_emailid(user_response["emailId"]):
			db.add_user_to_db(user_response)
			return jsonify({}), 200
		else:
			return jsonify({}), 409

# Function called when login operation is performed
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template("Login.html")

	email = request.form['email']
	if validate_user_emailid(email) == 0:
		if hashlib.sha1(request.form['password'].encode()).hexdigest() == user_db_data[email]["password"]:
			user = User()
			user.id = email
			flask_login.login_user(user)
			return redirect(url_for('Search'))
		
	return redirect("login_error")

# Function called for search operation
@app.route('/Search')
@flask_login.login_required
def Search():
	if request.method == "GET":
		cuisine_type = [{11:2},{22:2}]
		cuisine_response = requests.get("https://developers.zomato.com/api/v2.1/cuisines?city_id=4&lat=12.9716&lon=77.5946", headers={"content-type":"application/json", "user-key": "API-KEY"})
		cuisine_response = cuisine_response.json()
		restaurant_category = requests.get("https://developers.zomato.com/api/v2.1/categories", headers={"content-type":"application/json", "user-key": "API-KEY"})
		restaurant_category = restaurant_category.json()
		restaurant_type = requests.get("https://developers.zomato.com/api/v2.1/establishments?city_id=4&lat=12.9716&lon=77.5946", headers={"content-type":"application/json", "user-key": "API-KEY"})
		restaurant_type = restaurant_type.json()
		print("Result obtained")
		for key,value in cuisine_response.items():
			for i in  value:
				for sub_key, sub_value  in i.items():
					cuisine_type.append({sub_value["cuisine_name"]:["Cuisine",sub_value["cuisine_id"]]})
		for key,value in restaurant_category.items():
			for i in  value:
				for sub_key, sub_value  in i.items():
					cuisine_type.append({sub_value["name"]:["Category",sub_value["id"]]})
		for key,value in restaurant_type.items():
			for i in  value:
				for sub_key, sub_value  in i.items():
					cuisine_type.append({sub_value["name"]:["Type",sub_value["id"]]})

		return render_template("Search.html", result = cuisine_type)

# Fucntion called when a restaurant of a particular type is searched [Cuisine, Category etc.]
@app.route("/get_search_result", methods = ["GET"])
@flask_login.login_required
def get_search_result():
	if request.method == "GET":
		restaurants_list = []
		if request.args["type"] == 'Cuisine':
			restaurant_response	=requests.get("https://developers.zomato.com/api/v2.1/search?entity_id=4&entity_type=city&start=1&count=10&cuisines="
			 + request.args["id"], headers={"content-type":"application/json", "user-key": "API-KEY"})
			restaurant_response = restaurant_response.json()
			restaurant_response = restaurant_response["restaurants"]
			for i in restaurant_response:
				for key, value in i.items():
					restaurants_list.append({value["id"]: [value["name"], value["url"], value["cuisines"], value["user_rating"]["aggregate_rating"], 
						value["average_cost_for_two"], value["featured_image"], value["location"]["address"]]})
		elif request.args["type"] == 'Category':
			restaurant_response	=requests.get("https://developers.zomato.com/api/v2.1/search?entity_id=4&entity_type=city&start=1&count=10&category="
			 + request.args["id"], headers={"content-type":"application/json", "user-key": "API-KEY"})
			restaurant_response = restaurant_response.json()
		elif request.args["type"] == 'Type':
			restaurant_response	=requests.get("https://developers.zomato.com/api/v2.1/search?entity_id=4&entity_type=city&start=1&count=10&establishment_type="
			 + request.args["id"], headers={"content-type":"application/json", "user-key": "API-KEY"})
			restaurant_response = restaurant_response.json()
		else:
			print("Invalid")

		return render_template("Restaurants.html", result = restaurants_list)


# Function for getting the restaurant details
@app.route("/get_restaurant_detail/<restaurant_name>")
@flask_login.login_required
def get_restaurant_detail(restaurant_name):
	if request.method == "GET":
		print(restaurant_name)
		restaurant_response	=requests.get("https://developers.zomato.com/api/v2.1/restaurant?res_id=" + restaurant_name, 
			headers={"content-type":"application/json", "user-key": "API-KEY"})
		restaurant_response = restaurant_response.json()
		restaurant_detail = {}
		restaurant_detail[restaurant_response["R"]["res_id"]] = {"name" : restaurant_response["name"], "url" : restaurant_response["url"], "location" : restaurant_response["location"]["address"] +" "
		+ restaurant_response["location"]["locality"] + " " + restaurant_response["location"]["city"], "cuisines" : restaurant_response["cuisines"], "average_cost_for_two" : restaurant_response["average_cost_for_two"],
		"events_url" : restaurant_response["events_url"], "photos_url" : restaurant_response["photos_url"], "user_rating" : restaurant_response["user_rating"]["aggregate_rating"], 
		"featured_image" : restaurant_response["featured_image"], "has_online_delivery" : restaurant_response["has_online_delivery"], "is_delivering_now": restaurant_response["is_delivering_now"],
		"has_table_booking" : restaurant_response["has_table_booking"], "menu_url" : restaurant_response["menu_url"]}

		restaurant_review	=requests.get("https://developers.zomato.com/api/v2.1/reviews?res_id=" + restaurant_name, 
			headers={"content-type":"application/json", "user-key": "API-KEY"})
		restaurant_review = restaurant_review.json()
		restaurant_review = restaurant_review["user_reviews"]
		restaurant_review_dictionary = {}
		restaurant_review_dictionary[restaurant_name] = []
		restaurants_review_from_db = db.get_review_for_restaurant_from_db(restaurant_name)
		for i in restaurant_review:
			for key, value in i.items():
				restaurant_review_dictionary[restaurant_name].append({ "rating" : value["rating"], "review_text" : value["review_text"], "user_name" : value["user"]["name"]})
		for i in restaurants_review_from_db:
				restaurant_review_dictionary[restaurant_name].append({ "rating" : i[2], "review_text" : i[3], "user_name" : i[1]})

		if restaurant_detail[restaurant_response["R"]["res_id"]]["has_table_booking"] == 1:
			restaurant_detail[restaurant_response["R"]["res_id"]]["has_table_booking"] = "Yes"
		else:
			restaurant_detail[restaurant_response["R"]["res_id"]]["has_table_booking"] = "No"
		if restaurant_detail[restaurant_response["R"]["res_id"]]["is_delivering_now"] == 1:
			restaurant_detail[restaurant_response["R"]["res_id"]]["is_delivering_now"] = "Yes"
		else:
			restaurant_detail[restaurant_response["R"]["res_id"]]["is_delivering_now"] = "No"
		if restaurant_detail[restaurant_response["R"]["res_id"]]["has_online_delivery"] == 1:		
			restaurant_detail[restaurant_response["R"]["res_id"]]["has_online_delivery"] = "Yes"
		else:
			restaurant_detail[restaurant_response["R"]["res_id"]]["has_online_delivery"] = "No"

		return render_template("RestaurantDetail.html", restaurant_details = restaurant_detail, restaurant_review = restaurant_review_dictionary)


# Function for adding reviews
@app.route("/get_restaurant_detail/add_review", methods = ["POST"])
@flask_login.login_required
def add_review():
	if request.method == "POST":
		rating = request.form["rating"]
		review_text = request.form["review_text"]
		restaurant_id = request.form["restaurant_id_for_review"]
		print(flask_login.current_user.id, flask_login.current_user.name, rating, review_text, restaurant_id)
		db.add_review_to_db(flask_login.current_user.id, flask_login.current_user.name, rating, review_text, restaurant_id)
	return redirect("get_restaurant_detail/" + restaurant_id)

if __name__ == "__main__":
	app.run(debug=True)


