# How to run project

pip3 install -r requirements.txt

flask run

# Apt document 

https://127.0.0.1:5000/swagger-ui

# flask-migrate ( update table - add columms)

flask db stamp head

flask db migrate -m "Update user table"

flask db upgrade  

# FUNCTION SEARCH

search user information by First Name and Phone Number

# Validate

lastName - max 80 characters
firstName - max 80 characters
phoneNumber - max 11 characters
address - max 300 characters
