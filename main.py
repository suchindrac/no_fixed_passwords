from flask import Flask, request, render_template
import json
import random
import string

app = Flask(__name__)

@app.route("/set_password", methods=["POST"])
def set_password():
    username = request.form.getlist("username")[0]
    index1 = request.form.getlist("index1")[0]
    index2 = request.form.getlist("index2")[0]
    index3 = request.form.getlist("index3")[0]
    index4 = request.form.getlist("index4")[0]
    index5 = request.form.getlist("index5")[0]
    
    details = { "username": username,
                "index1": index1,
                "index2": index2,
                "index3": index3,
                "index4": index4,
                "index5": index5
              }

    try:
        with open("indices.json") as fd:
            try:
                prev_details = json.load(fd)
            except json.decoder.JSONDecodeError:
                prev_details = []
    except FileNotFoundError:
        prev_details = []
            
    if len(prev_details) != 0:
        set_value = False
        for i in range(len(prev_details)):
            if prev_details[i]["username"] == username:
                prev_details[i] = details
                set_value = True
                break
        if not set_value:
            prev_details.append(details)
    else:
        prev_details.append(details)
        
    with open("indices.json", "w+") as fd:
        json.dump(prev_details, fd)
    
    return "True"
    
    
@app.route("/show_login", methods=["GET"])
def show_login_page():
    rand_string_shown = ""
    for i in range(25):
        temp = ''.join(random.choices(string.ascii_uppercase + \
                                      string.ascii_lowercase + \
                                      string.digits, k=10))
        rand_string_shown += f"\n{temp}"

    rand_string = rand_string_shown.replace("\n", "")
        
    details = {
        "username": "NEW",
        "rand_string": rand_string
    }
            
    with open("rand_strings.json", "w+") as fd:
        json.dump(details, fd)

    return render_template("login.html", random_text=rand_string_shown)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.getlist("username")[0]
    password = request.form.getlist("password")[0]
    rand_string_shown = request.form.getlist("random_text")
    rand_string_shown = rand_string_shown[0]
    rand_string = rand_string_shown.replace("\r\n", "")
    
    fd_p = open("indices.json", "r")

    indices = None
    try:
        indices = json.load(fd_p)
        users = [x["username"] for x in indices]
    except json.decoder.JSONDecodeError:
        users = []

    found_password = ""
    
    if username in users:
        for elem in indices:
            if elem["username"] == username:
                for i in ("index1", "index2", "index3", "index4", "index5"):
                    found_password += rand_string[int(elem[i])]

    print(found_password, password)

    if found_password == password:
        return "Login successful"
    else:
        return "Login failed"
    
@app.route("/show_set_password", methods=["GET"])
def show_set_password_page():
    return render_template("set_password.html")

if __name__ == "__main__":
    app.run(debug=True)
