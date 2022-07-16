from flask import Flask, request, render_template
import json, os, hashlib

app = Flask(__name__)


def encoder(text):
    result = hashlib.sha256(text.encode('utf-8'))
    result = result.hexdigest()
    return result


def is_valid_email(email):
    if "@" in email and "." in email:
        return True
    else:
        return False


def is_valid(name, email, pwd):
    if len(name) >= 1 and is_valid_email(email) and len(pwd) >= 1:
        return True
    else:
        return False


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signin", methods=["POST"])
def signin():
    file_list = os.listdir("./users_data")
    for file in file_list:
        if file[:-15] == request.form["email"]:
            with open(f"./users_data/{file}", "r", encoding='utf-8') as f:
                json_data = json.load(f)
                user_pwd = encoder(request.form['password'])
            if json_data['user_pwd'] == user_pwd:
                return "Loginned"
            else:
                return "Wrong Password"
    return "You need to register!"


@app.route("/register", methods=["GET"])
def post():
    return render_template('register.html')


@app.route("/signup", methods=["POST"])
def signup():
    email_path = "./users_data/users_email.json"
    if request.method == "POST":
        file_list = os.listdir("./users_data")
        if request.form["email"] + "_user_data.json" in file_list:
            return "There is an account with that e-mail"
        else:
            user_name = request.form['name']
            user_email = request.form['email']
            user_pwd = encoder(request.form['password'])
            if is_valid(user_name, user_email, user_pwd):
                # building json form
                user_data = {}
                user_data['user_name'] = user_name
                user_data['user_email'] = user_email
                user_data['user_pwd'] = user_pwd
                # Save the file as json
                file_name = f"./users_data/{user_email}_user_data.json"
                with open(file_name, "w", encoding='utf-8') as file:
                    json.dump(user_data, file, indent="\t", ensure_ascii=False)
                return "Success"
            else:
                return "Enter Valid values"
    else:
        return "Wrong Connection"


@app.route("/method", methods=['GET', 'POST'])
def method():
    if request.method == "GET":
        return "GET REQUEST"
    if request.method == "POST":
        return "POST REQUEST"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)



