from itertools import permutations
from utilities import *
from users_functions import *

Wt=((68+2) % 100)/100
We=1-Wt

k = task3["k"]
T=task3["T"]
M=task3["M"]

step2_done=False

app = Flask(__name__)


@app.route("/start", methods=["POST"])
def start():
    global step2_done
    step2_done=False
    try:
        step_1(k, T, M, Wt, We, t_hat, USER_3, 1)
        return jsonify({"status": "started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/result", methods=["POST"])
def receive_result():
    global step2_done
    try:
        data = request.json
        T_matrix = data.get("T")
        E_matrix=data.get("E")
        
         #compute actual utility value
        actual_utility=compute_actual_utility(T_matrix,E_matrix,Wt,We,USER_3)
        print("------ Actual utility value: ",actual_utility," ------")
        if step2_done==False:
            step2_done=True
            step_2(k,T,M,Wt,We,T_matrix,USER_3,2)
        
        return jsonify({"status": "started"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
   
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)