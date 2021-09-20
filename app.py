from flask import Flask
from flask import render_template, request, session, redirect, url_for
import os
from utl.dbFunction import *

app = Flask(__name__)
createDB()

@app.route("/", methods=["POST","GET"])
def root():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        userValid = checkUser(username, password)
        if username == "" or password =="":
            return render_template('homepage.html')
        if userValid:
            return redirect(url_for("interactivePage", username=username))

    return render_template('homepage.html')


# removes session data for username
@app.route("/register", methods=["POST","GET"])
def createAccount():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not checkUsername(username):
            addUser(username, password)
            return redirect(url_for("root"))

    return render_template("register.html")

@app.route("/interactivepage/<username>", methods=["POST", "GET"])
def interactivePage(username):
    if request.method == "POST":
        loc0 = request.form["loc0"]
        loc1 = request.form["loc1"]
        loc2 = request.form["loc2"]
        loc3 = request.form["loc3"]
        loc4 = request.form["loc4"]

        mode1 = request.form["mode1"]
        mode2 = request.form["mode2"]
        mode3 = request.form["mode3"]
        mode4 = request.form["mode4"]

        templocations = [loc0, loc1, loc2, loc3, loc4]
        locations = []
        for loc in templocations:
            if loc != '':
                locations.append(loc)

        tempmodes = [mode1, mode2, mode3, mode4]
        modes = []
        for mode in tempmodes:
            if mode != '':
                modes.append(mode)




        #print(schedule)
        if len(modes)==0 or len(locations)==0:
            return render_template("interactivepage.html", lenloc=-1, loc=locations, m=modes, username=username,
            walkedMiles=None, bikedMiles=None,drivenMiles=None,savedCO2=None,burnedCalories=None)
        if len(locations) - len(modes) !=1:
            return render_template("interactivepage.html", lenloc=-1, loc=locations, m=modes, username=username,
            walkedMiles=None, bikedMiles=None,drivenMiles=None,savedCO2=None,burnedCalories=None)
        userDataToDB(username, locations, modes)
        locations_string = "["
        for location in locations[:-1]:
            locations_string+="'"+location+"'"+","
        locations_string+="'" + locations[-1] + "'" + "]"

        modes_string = "["
        for mode in modes[:-1]:
            modes_string += "'" + mode + "'"+ ","
        modes_string+="'" + modes[-1] + "'" + "]"

        command = "python3 backend/computation.py " + str(username) + " " + locations_string + " " + modes_string
        os.system(command)
        tup=dbDataToFrontend(username)
        walkedMiles=tup[0]
        bikedMiles=tup[1]
        drivenMiles=tup[2]
        savedCO2=tup[3]
        burnedCalories=tup[4]
        printDB()
        return render_template("interactivepage.html", lenloc=len(locations), loc=locations, m=modes, username=username,
        walkedMiles=walkedMiles, bikedMiles=bikedMiles,drivenMiles=drivenMiles,savedCO2=savedCO2,burnedCalories=burnedCalories)



    return render_template("interactivepage.html", lenloc=-1,username=username,
    walkedMiles=None, bikedMiles=None,drivenMiles=None,savedCO2=None,burnedCalories=None)

if __name__ == "__main__":
    app.run(debug=True)
