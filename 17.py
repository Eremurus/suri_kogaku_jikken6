from numpy.random import random
import pandas as pd
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

#忘却係数
gamma = 0.99

#実際のy を生成する関数
def y_k_real(k):
    belnui = np.random.randint(0,2)
    if belnui == 0:
        w = -1.0
    else:
        w = 1.0
    return np.sin(0.0001 * k) + w

#忘却最小二乗法の関数
def boukyaku_saisyou_nijou(Phi, theta, y):
    K = Phi / (1.0 + Phi)
    theta = theta + K * (y - theta)
    Phi = Phi / gamma - K * Phi / gamma
    return theta, Phi

#パラメータ
theta = 0.0
epsilon = 10 ** (-6)
Phi = 1.0 / epsilon
theta_list = []
k_list = []
sink_list = []

#それぞれのk に対して予測値を計算
for k in range(1, 10001):
    k_list.append(k)
    y = y_k_real(k)
    theta, Phi = boukyaku_saisyou_nijou(Phi, theta, y)
    theta_list.append(theta)
    sink_list.append(np.sin(k * 0.0001))

#プロット
fig, ax = plt.subplots(facecolor="w")
ax.plot(k_list, theta_list, label="estimate")
ax.plot(k_list, sink_list, label="real theta")
ax.legend()

plt.xlabel("k")
plt.ylabel("theta")
plt.show()
