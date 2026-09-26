# shared data across users and the resource manager
n_tasks=3
m_resources=5

#endpoint_url = "http://127.0.0.1:5000"

USER_1=0
USER_2=1
USER_3=2

ROUNDS=2

prices = [1.0, 1.2, 1.5, 1.8, 2.0]

t_hat = [
    [6.0, 5.0, 4.0, 3.5, 3.0],
    [5.0, 4.2, 3.6, 3.0, 2.8],
    [4.0, 3.5, 3.2, 2.8, 2.4]
]

task1= {"k": 2, "T": 500, "M": 20}

task2= {"k": 3, "T": 300, "M": 30}

task3= {"k": 4, "T": 800, "M": 30} # T is time constraint in seconds and M is money constraint