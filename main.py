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

    with open("passwords.json") as fd:
        try:
            prev_details = json.load(fd)
        except json.decoder.JSONDecodeError:
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
    with open("passwords.json", "w") as fd:
        json.dump(prev_details, fd)
    
    return "True"
    
    
@app.route("/show_login", methods=["GET"])
def show_login_page():
    rand_string_show = ""
    for i in range(50):
        temp = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
        rand_string_show += f"\n{temp}"

    rand_string = rand_string_show.replace("\n", "")
    
    with open("rand_strings.json") as fd:
        try:
            prev_details = json.load(fd)
        except json.decoder.JSONDecodeError:
            prev_details = []

        set_value = False
        if len(prev_details) != 0:
            for i in range(len(prev_details)):
                if prev_details[i]["username"] == "NEW":
                    details = {
                                "username": "NEW",
                                "rand_string": rand_string
                              }
                    prev_details[i] = details
                    set_value = True
                    break

            if not set_value:
                details = {
                            "username": "NEW",
                            "rand_string": rand_string
                          }
                prev_details.append(details)
        else:
            details = {
                        "username": "NEW",
                        "rand_string": rand_string
                      }
            prev_details.append(details)
            
    with open("rand_strings.json", "w") as fd:
        json.dump(prev_details, fd)

    return render_template("login.html", random_text=rand_string_show)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.getlist("username")[0]
    password = request.form.getlist("password")[0]
    rand_string_shown = request.form.getlist("random_text")
    
    fd_s = open("rand_strings.json", "r")
    fd_p = open("passwords.json", "r")
    
    try:
        rand_strings = json.load(fd_s)
    except json.decoder.JSONDecodeError:
        rand_strings = []

    try:
        users = json.load(fd_p)
        users = [x["username"] for x in users]
    except json.decoder.JSONDecodeError:
        users = []

    fd_p = open("passwords.json", "r")
        
    rand_string_comp = ""
    
    for elem in rand_strings:
        if elem["username"] == "NEW":
            rand_string_comp = elem["rand_string"]
            break
        
    if rand_string_comp == "":
        return "Don't have a random string to compare with"
    
    found_password = ""
    
    if username in users:
        indices = json.load(fd_p)
        for elem in indices:
            if elem["username"] == username:
                for i in ("index1", "index2", "index3", "index4", "index5"):
                    found_password += rand_string_comp[int(elem[i])]

    print(found_password, password)

    for i in range(len(rand_strings)):
        if rand_strings[i]["username"] == "NEW":
            rand_strings[i]["username"] = username
            with open("rand_strings.json", "w") as fd:
                json.dump(rand_strings, fd)
            
    if found_password == password:
        return "Login successful"
    else:
        return "Login failed"
    
@app.route("/show_set_password", methods=["GET"])
def show_set_password_page():
    return render_template("set_password.html")

if __name__ == "__main__":
    app.run(debug=True)
