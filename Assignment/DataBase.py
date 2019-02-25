import sqlite3
import hashlib
# Function for adding user to db
def add_user_to_db(user):
	connection_state = sqlite3.connect("RestaurantReview.db")
	cursor = connection_state.cursor()
	cursor.execute("INSERT INTO User (firstname, lastname, emailId, password) VALUES (?, ?, ?, ?)",
		(user['firstName'], user['lastName'], user['emailId'], hashlib.sha1((user['password']).encode()).hexdigest()))
	connection_state.commit()
	connection_state.close()


# Function for getting review from db
def get_review_for_restaurant_from_db(restaurant_id):
	connection_state = sqlite3.connect("RestaurantReview.db")
	cursor = connection_state.cursor()
	cursor.execute("SELECT * FROM Review where restaurant_id = ?",(restaurant_id,))
	restaurants_review_from_db = cursor.fetchall()
	connection_state.commit()
	connection_state.close()
	return restaurants_review_from_db

# function for adding review to db
def add_review_to_db(user_mail_id, user_name, rating, review_text, restaurant_id):
	try:
		connection_state = sqlite3.connect("RestaurantReview.db")
		cursor = connection_state.cursor()
		cursor.execute("INSERT INTO Review (user_id, user_name, rating, review, restaurant_id) VALUES (?, ?, ?, ?, ?)",
			(user_mail_id, user_name, rating, review_text, restaurant_id))
		connection_state.commit()
		connection_state.close()
		return 1
	except:
		return 0