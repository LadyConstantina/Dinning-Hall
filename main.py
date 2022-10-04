from flask import Flask, request
from dinning_hall import Dinning_Hall
import time
import threading

table_list = [
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    }
]

dinning_hall = Dinning_Hall(table_list, 6)


app = Flask(__name__)
@app.route("/distribution", methods = ["POST"])
def distribution():
    if request.method == "POST":
        order_info = request.json
        print("Order with id "+str(order_info["order_id"])+" was prepared in "+str(time.time() - order_info["pick_up_time"]))
        dinning_hall.free_table(order_info["table_id"])
    
    return "b"

if __name__ == "__main__":
    # Running a thread for the flask application.
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=5000, host="127.0.0.1",)).start()

    # Creating the dinning hall object and running the main function.
    dinning_hall.Run_restaurant()
    
