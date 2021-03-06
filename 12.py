import pandas as pd
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

n = 2
N = 1000 
V = np.array([[100.0, 0.0],[0.0, 1.0]])

#基底関数
def phi(x):
    kitei = np.array([[x**0, x**0],[x, x**2]])
    return kitei.T

#6_5 の方法でパラメータを予測、誤差共分散行列を求める
def calc_theta_6_5(x, y,data_num):
    #パラメータ
    Phi = np.array([[0.0,0.0],[0.0,0.0]])
    for i in range(data_num):
        Phi += np.dot(phi(x)[i].T, phi(x)[i])
    Phi = la.inv(Phi)
    
    migi = np.array([0.0,0.0])
    for i in range(data_num):
        migi += np.dot(phi(x)[i].T, y[i])
    
    theta = np.dot(Phi, migi)

    #誤差共分散行列
    Err_mat = np.array([[0.0,0.0],[0.0,0.0]])

    for i in range(data_num):
        phi_v = np.dot(phi(x)[i].T, V)
        phi_v_phi = np.dot(phi_v, phi(x)[i])
        phi_v_phi_Phi = np.dot(phi_v_phi, Phi)
        Err_mat += phi_v_phi_Phi
    Err_mat = np.dot(Phi, Err_mat)

    return theta, Err_mat

#6_17の方法でパラメータを予測、誤差共分散行列を求める
def calc_theta_6_17(x, y, data_num):
    #パラメータ
    Q = la.inv(V)
    Phi = np.array([[0.0,0.0],[0.0,0.0]])
    for i in range(data_num):
        phi_q = np.dot(phi(x)[i].T, Q)
        Phi += np.dot(phi_q, phi(x)[i])
    Phi = la.inv(Phi)
    migi = np.array([0.0,0.0])
    for i in range(data_num):
        phi_q = np.dot(phi(x)[i].T, Q)
        migi += np.dot(phi_q, y[i])

    theta = np.dot(Phi, migi)

    #誤差共分散行列
    Err_mat = np.array([[0.0,0.0],[0.0,0.0]])
    Phi_dash = np.array([[0.0, 0.0],[0.0, 0.0]])
    for i in range(data_num):
        phi_q = np.dot(phi(x)[i].T, Q)
        phiqphi = np.dot(phi_q, phi(x)[i])
        Phi_dash += phiqphi
    Phi_dash = la.inv(Phi_dash)
    for i in range(data_num):
        kari = np.dot(phi(x)[i].T, Q)
        kari = np.dot(kari, V)
        kari = np.dot(kari, Q.T)
        kari = np.dot(kari, phi(x)[i])
        kari = np.dot(kari, Phi_dash.T)
        Err_mat += kari
    Err_mat = np.dot(Phi_dash ,Err_mat)
    '''
    for i in range(data_num):
        phi_v = np.dot(phi(x)[i].T, V)
        phi_v_phi = np.dot(phi_v, phi(x)[i])
        phi_v_phi_Phi = np.dot(phi_v_phi, Phi)
        Err_mat += phi_v_phi_Phi
    Err_mat = np.dot(Phi, Err_mat)
    '''
    return theta, Err_mat

#データ読み込み
df = pd.read_csv("./suri_jikken6_data/mmse_kadai5.txt",header=None)
data = np.array(df)

x = np.array(data[:,0])
y = np.array(data[:,1:3])

#6_5 でパラメータを求める
ans_6_5 = calc_theta_6_5(x, y, N)
print(ans_6_5[0], ans_6_5[1])

#6_17でパラメータを求める
ans_6_17 = calc_theta_6_17(x, y, N)
print(ans_6_17[0], ans_6_17[1])

#プロットのためのリスト
theta_0_list = []
theta_1_list = []
theta_2_list = []
theta_3_list = []
N_list = []
real_ans_0_list = []
real_ans_1_list = []
real_ans_2_list = []
real_ans_3_list = []

#プロット
for data_num in range(1,N+1):
    #data_num = 2 ** k
    N_list.append(data_num)
    real_ans_0_list.append(3.0)
    real_ans_1_list.append(-2.0)
    real_ans_2_list.append(3.0)
    real_ans_3_list.append(-2.0)

    x = np.array(data[0:data_num,0])
    y = np.array(data[0:data_num,1:3])

    theta_0 = calc_theta_6_5(x, y, data_num)[0][0]
    theta_1 = calc_theta_6_5(x, y, data_num)[0][1]
    theta_2 = calc_theta_6_17(x, y, data_num)[0][0]
    theta_3 = calc_theta_6_17(x, y, data_num)[0][1]

    theta_0_list.append(theta_0)
    theta_1_list.append(theta_1)
    theta_2_list.append(theta_2)
    theta_3_list.append(theta_3)

fig, ax = plt.subplots(facecolor="w")
ax.plot(N_list, theta_0_list, label="estimate")
ax.plot(N_list, real_ans_0_list, label="true")
ax.legend()

plt.xscale('log')
plt.xlabel('N')
plt.ylabel('theta')
plt.show()

fig, ax = plt.subplots(facecolor="w")
ax.plot(N_list, theta_1_list, label="estimate")
ax.plot(N_list, real_ans_1_list, label="true")
ax.legend()

plt.xscale('log')
plt.xlabel('N')
plt.ylabel('theta')
plt.show()

fig, ax = plt.subplots(facecolor="w")
ax.plot(N_list, theta_2_list, label="estimate")
ax.plot(N_list, real_ans_2_list, label="true")
ax.legend()

plt.xscale('log')
plt.xlabel('N')
plt.ylabel('theta')
plt.show()

fig, ax = plt.subplots(facecolor="w")
ax.plot(N_list, theta_3_list, label="estimate")
ax.plot(N_list, real_ans_3_list, label="true")
ax.legend()

plt.xscale('log')
plt.xlabel('N')
plt.ylabel('theta')
plt.show()

'''

(6.5)による推定誤差共分散行列は
[[ 0.03514546 -0.01251624]
[-0.01251624  0.01086049]]

(6.17)による推定誤差共分散行列は
[[ 0.00147742 -0.00050005]
[-0.00050005  0.00051312]]
'''