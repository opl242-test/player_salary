from classifier import Classifier
from flask import Flask, render_template, request
# from flask_socketio import SocketIO

app = Flask(__name__)
# socketio = SocketIO(app)

# print("Load classifier")
classifier = Classifier()
# print("Classifier is successfully loaded")
# print(time.time() - start_time, "seconds")


@app.route("/", methods = ["POST", "GET"])
def index_page(player_id=66):
    predicted_salary = 0
    if request.method == "POST":
        try:
            player_id = int(request.form['player_id'])
            predicted_salary = classifier.predict_salary(player_id)
        except:
            pass

    return render_template(
        'index.html',
        predicted_salary=predicted_salary
    )

if __name__ == "__main__":
    # socketio.run(app)
    app.run()