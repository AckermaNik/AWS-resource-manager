import time
import requests
from utilities import *
from itertools import permutations
from flask import Flask, jsonify,request
import boto3
import json
from config import get_env


sqs = boto3.client("sqs", region_name=get_env("AWS_REGION", "us-east-1"))
QUEUE_URL = get_env("AWS_SQS_QUEUE_URL")

def passes_constraints(b,user_i,total_price,max_time,k,T,M,t_hat):

    for i in range(k):
            for j in range(m_resources):
                if b[i][j]==1:
                    if(t_hat[user_i][j]>max_time[0]): max_time[0]=t_hat[user_i][j]
    #print("Max time ",max_time[0],"for b: ",b)
    if max_time[0] > T:
        return False

    for i in range(k):
        for j in range(m_resources):
            total_price[0] += prices[j] * t_hat[user_i][j] * b[i][j]
    #print("Total price ",total_price[0],"for b: ",b)
       
    if total_price[0] > M:
        return False
    
    return True


def compute_initial_utility(total_price,max_time,Wt,We):
    return round(1/(Wt*max_time[0] + We*total_price[0]),2)

def compute_actual_utility(T,E,Wt,We,user):
    max_t=-1
    for j in range(m_resources):
        if T[user][j]>max_t: max_t=T[user][j]
    if max_t==0: 
        return 0.0
    else:
        return round(1/(Wt*max_t + We*sum(E[user][j] for j in range(m_resources))),2)


            
def step_1(k,T,M,Wt,We,t_hat,user,round_id):

    b_matrices = []
    a=[0]*5

    #generate b matrixes
    for assignment in permutations(range(m_resources), k): #(1,3) k(1)->1, k(2)->3
        matrix_b = [[0]*5 for _ in range(k)]
        for row, col in enumerate(assignment): #make (row,collumn) pairs
            matrix_b[row][col] = 1
            
        #print(matrix_b)
        b_matrices.append(matrix_b)

    #evaluate b matrixes
    valid_matrices = {}

    for index,b in enumerate(b_matrices):
        total_price=[0]
        max_time=[-10]
        if passes_constraints(b,user,total_price,max_time,k,T,M,t_hat):
            utility = compute_initial_utility(total_price,max_time,Wt,We)
            #print("----b that passes: ",b,"with utility: ",utility)  
            valid_matrices[index] = {
                "utility": utility,
                "b": b
            }
            
    if not valid_matrices:
        print("No valid matrices found\n")
        selected_b=[[0]*5 for _ in range(k)]
    else:           
        max_utility_index = max(valid_matrices, key=lambda i: valid_matrices[i]["utility"])
        print("------ Initial utility:",valid_matrices[max_utility_index]["utility"]," ------")   
        selected_b = valid_matrices[max_utility_index]["b"]

    #create a from selected_b matrix      
    for i in range(k):
        for j in range(m_resources):
            if selected_b[i][j]==1:
                a[j]=1
                
    print("Matrix:  ",a)
    
    message = {
        "user_id": user,
        "matrix": a,
        "round":round_id,
        "t_hat":t_hat
    }

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    return jsonify({"status": "submitted", "user": USER_1})

    #compute T and E
    #requests.post(endpoint_url+"/a_matrix",params={"user": user,"round":round_id}, json={"matrix": a,"t_hat":t_hat})

    #get T and E
    # long polling until result is ready
    # while True:        
    #     try:
    #         resp = requests.get(f"{endpoint_url+"/result"}",params={
    #         "wait": "true",
    #         "round": round_id,
    #         "user":user,
    #         }, timeout=60)
            
    #         data = resp.json()

    #         if data["status"] == "ready":
    #             T_matrix=data["T"]
    #             E_matrix=data["E"]
    #             print("T:", T_matrix)
    #             print("E:", E_matrix)
    #             break
    #         print("waiting......")
    #     except requests.exceptions.Timeout:
    #         continue        
    #     time.sleep(1)


def step_2(k,T,M,Wt,We,t_matrix_new,user,round_id):
    
    t_new = [[0]*m_resources for _ in range(n_tasks)]
    
    for j in range(m_resources):
        col_sum = 0
        for r in range(n_tasks):
            col_sum += t_matrix_new[r][j]

        for i in range(n_tasks):
            t_new[i][j] = round(t_hat[i][j] + col_sum / n_tasks,2)
    print()    
    print("NEW t_hat: ",t_new)
    step_1(k,T,M,Wt,We,t_new,user,round_id)
