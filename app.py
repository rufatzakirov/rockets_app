from flask import Flask
from flask import render_template
import socket
import random
import os
import argparse

app = Flask(__name__)

ROCKET_PORT = os.environ.get('ROCKET_PORT') or '8080'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
VERSION_ENV = os.environ.get('VERSION') or 'v0.1'

rockets = {
    "small": "small",
    "average": "average",
    "big": "big",
}

rockets_list = ",".join(rockets.keys())

rocket_env = os.environ.get('ROCKET_SIZE')

rocket = random.choice(["small","average","big"])

@app.route("/")
def main():
    #return 'Hello'
    print(rocket)
    return render_template('hello.html', name=socket.gethostname(), rocket=rockets[rocket], version=VERSION_ENV)

@app.route("/info")
def info():
    #return 'Info'
    return "App Version: {} ; Rocket Size: {} ; ".format(VERSION_ENV, rocket)

@app.route("/version")
def version():
    #return 'Ver'
    return "App Version: {} ;".format(VERSION_ENV)



if __name__ == "__main__":

    print(" Командир, мы предоставим вам ракеты по вашему запросу! \n"
          " Сделать заказ можно двумя путями: \n"
          "\n"
          " 1. Из командной строки с ключом --size. Доступные размеры: " + rockets_list + " \n"
          " 2. Установив переменную окружения ROCKET_SIZE. Доступные размеры: " + rockets_list + " \n"
          " 3. Если выбор не будет сделан, мы выдадим вам ракету сами! \n"
          " Внимание, данные из командной строки имеют самый высокий приоритет.\n"
          "\n"
          "")

    # Check for Command Line Parameters for size
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', required=False)
    args = parser.parse_args()

    if args.size:
        print("Size from command line argument =" + args.size)
        rocket = args.size
        if rocket_env:
            print("A size was set through environment variable -" + rocket_env + ". However, size from command line argument takes precendence.")
    elif rocket_env:
        print("No Command line argument. Size from environment variable =" + rocket_env)
        rocket = rocket_env
    else:
        print("No command line argument or environment variable. Picking a Random Size =" + rocket)

    # Check if input size is a supported one
    if rocket not in rockets:
        print("Rocket not supported. Received '" + rocket + "' expected one of " + rockets_list)
        exit(1)

    # Run Flask Application
    app.run(host="0.0.0.0", port=ROCKET_PORT)