from copy import deepcopy
import time
from  utilities import *
import requests
from flask import Flask, request, jsonify
from config import get_env


#Flask server

USER_ENDPOINTS = {
    "0": get_env("USER_0_ENDPOINT"),
    "1": get_env("USER_1_ENDPOINT"),
    "2": get_env("USER_2_ENDPOINT")
}

# a_total_matrix = [[] for _ in range(3)]
# checked_users=[[0]*n_tasks for _ in range(2)]
# result_ready = [False]*ROUNDS
# users_done=[False]*n_tasks

app = Flask(__name__)

def check_users(round_id,checked_users):
    for j in range(n_tasks):
        if checked_users[round_id-1][j]==0:
            return False
    return True

def check_ready_users(round_id,result_ready):
     return result_ready[round_id-1]

def check_if_users_done(users_done):
    for i in range(n_tasks):
        if users_done[i]!=True:
            return False
    return True

@app.route('/compute', methods=['POST'])
def receive_data(): 
    try:
        T = [[0]*m_resources for _ in range(n_tasks)]
        E = [[0]*m_resources for _ in range(n_tasks)]
        a_total_matrix = [None] * 3
        
        data =  request.get_json(force=True)
        round_id = data["round"]
        for entry in data["matrix"]:
            uid = entry["user_id"]
            a_total_matrix[uid] = entry["matrix"]
        t_hat_received = data["t_hat"]
        
        assert len(a_total_matrix) == n_tasks
        assert all(len(row) == m_resources for row in a_total_matrix)
    
        for i in range(n_tasks):
            for j in range(m_resources):
                if a_total_matrix[i][j]== 0:
                    T[i][j]=E[i][j]=0
                else:
                    T[i][j]= round(sum(a_total_matrix[k][j] for k in range(n_tasks)) * t_hat_received[i][j],2)
                    E[i][j]=round(a_total_matrix[i][j]* t_hat_received[i][j]*prices[j],2)
        
        print("T: ",T)
        print()
        print()
        print("E: ",E)
        
        for user_id, url in USER_ENDPOINTS.items():
            payload = {
                "round": round_id,
                "T": T,
                "E": E
            }            
            try:
                r = requests.post(url, json=payload, timeout=5)
                print(f"Sent results to user {user_id}, status {r.status_code}")
            except Exception as e:
                print(f"Failed to send to user {user_id}: {e}")
        
        return jsonify({"status": "completed"})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# def receive_data():
#  #global result_ready, T, E, a_total_matrix,checked_users
    
#     user = int(request.args.get("user"))
#     round_id=int(request.args.get("round"))
#     #checked_users[round_id-1][user]=1
    
#     data = request.json  # Flask parses the JSON automatically to dictionary
#     matrix_received = data.get("matrix")
#     t_hat_received=data.get("t_hat")
#     a_total_matrix[user]=matrix_received
#     print(f"Received array: {matrix_received}")
    
#     if check_users(round_id,checked_users):
#         for i in range(n_tasks):
#             for j in range(m_resources):
#                 if a_total_matrix[i][j]== 0:
#                     T[i][j]=0
#                 else:
#                     T[i][j]= round(sum(a_total_matrix[k][j] for k in range(n_tasks)) * t_hat_received[i][j],2)
#                 E[i][j]=round(a_total_matrix[i][j]* t_hat_received[i][j]*prices[j],2)
#         result_ready[round_id-1]=True
        
#     return jsonify({"status": "ok"}), 200

# TIMEOUT=50
# @app.route('/result', methods=['GET'])
# def return_T_E():
#     global result_ready, T, E,a_total_matrix,checked_users,users_done
#     wait = request.args.get("wait", "false") == "true" #the query parameter is string and to turn it to boolean we must do =="true"
#     round_id=request.args.get("round", type=int)
#     user=request.args.get("user", type=int)
#     start = time.time()

#     while wait and time.time() - start <= TIMEOUT:
        
#         if check_ready_users(round_id,result_ready):
            
#             if round_id==2: users_done[user]=True
#             T_temp = deepcopy(T)
#             E_temp = deepcopy(E)
#             #reset global variables
#             if round_id==2 and check_if_users_done(users_done): 
#                 a_total_matrix = [[] for _ in range(3)]
#                 checked_users=[[0]*n_tasks for _ in range(2)]
#                 T = [[0]*m_resources for _ in range(n_tasks)]
#                 E = [[0]*m_resources for _ in range(n_tasks)]
#                 result_ready = [False]*ROUNDS           
#                 users_done=[False]*n_tasks
#             return jsonify({
#                 "status": "ready",
#                 "T": T_temp,
#                 "E": E_temp
#             })
#         time.sleep(1)

#     return jsonify({"status": "waiting"})
