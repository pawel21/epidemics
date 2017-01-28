import matplotlib.pyplot as plt
import  numpy as np
from scipy.integrate import odeint

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Helvetica'
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.unicode'] = True
plt.rcParams.update({'font.size': 20})
plt.rcParams['text.latex.preamble'] = r'\usepackage[T1]{polski}'


# P - podatni, którzy nie są jeszcze chodzy
# N - chorzy i są nosicielami
# W - uzdrowieni, nie są już podatni
# M - zgodny
# a - prawdopodbieństwo zakażenia
# b - szybkośc wyzdrowienia
# alpha - natularne urodzenia
# beta - natularne zgony

P_0 = 1000
N_0 = 1
W_0 = 1
M_0 = 1

a = 0.0005
b = 1/10.0
z = 0.015
alpha = 0.0005
beta = 0.0001
gamma = 0.05


def uklad_rownan(y, t, a, b, z, alpha, beta):
    P, N, W, M = y
    dP_dt = -a*N*P + alpha*(P + N + W)
    dN_dt = a*N*P - b*N - z*N
    dW_dt = b*N
    dM_dt = z*N + beta*(P + N + W)
    return dP_dt, dN_dt, dW_dt, dM_dt

def uklad_rownan_szczepienia(y, t, a, b, z, alpha, beta, gamma):
    P, N, W, M = y
    dP_dt = -a * N * P + alpha * (P + N + W) - gamma * P  # - 0.05*(P+N+W)
    dN_dt = a * N * P - b * N - z * N
    dW_dt = b * N + gamma * P
    dM_dt = z * N + beta * (P + N + W)
    return dP_dt, dN_dt, dW_dt, dM_dt


czas_w_dniach = np.linspace(0, 90, 1000)
y_0 = P_0, N_0, W_0, M_0
rozwiazanie = odeint(uklad_rownan, y_0, czas_w_dniach, args=(a, b, z, alpha, beta))
P, N, W, M = rozwiazanie.T


fig = plt.figure(facecolor='w')
ax = fig.add_subplot(121, axis_bgcolor='#dddddd', axisbelow=True)
ax.plot(czas_w_dniach, P, 'b', alpha=0.5, lw=2, label="Podatni")
ax.plot(czas_w_dniach, N, 'r', alpha=0.5, lw=2, label="Zarażeni")
ax.plot(czas_w_dniach, W, 'g', alpha=0.5, lw=2, label="Uzdrowieni")
ax.plot(czas_w_dniach, M, 'k', alpha=0.5, lw=2, label="Zgony")
ax.set_ylim([0, 1250])
ax.set_xlabel("Czas [dni]")
ax.set_ylabel("Liczba osób")
ax.set_title("Bez szczepienia")
ax.text(60, 600, 'a={0}\nb={1} \nz={2} \n alpha={3} \n beta={4}'.format(a, b, z, alpha, beta),
        bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
plt.legend(loc="upper center", prop={'size':18})

czas_w_dniach = np.linspace(0, 90, 1000)
y_0 = P_0, N_0, W_0, M_0
rozwiazanie_s = odeint(uklad_rownan_szczepienia, y_0, czas_w_dniach, args=(a, b, z, alpha, beta, gamma))
P_s, N_s, W_s, M_s = rozwiazanie_s.T

ax2 = fig.add_subplot(122, axis_bgcolor='#dddddd', axisbelow=True)
ax2.plot(czas_w_dniach, P_s, 'b', alpha=0.5, lw=2, label="Podatni")
ax2.plot(czas_w_dniach, N_s, 'r', alpha=0.5, lw=2, label="Zarażeni")
ax2.plot(czas_w_dniach, W_s, 'g', alpha=0.5, lw=2, label="Uzdrowieni")
ax2.plot(czas_w_dniach, M_s, 'k', alpha=0.5, lw=2, label="Zgony")
ax2.set_ylim([0, 1250])
ax2.set_xlabel("Czas [dni]")
ax2.set_ylabel("Liczba osób")
ax2.set_title("Szczepienie")
ax2.text(60, 600, 'a={0}\nb={1} \nz={2} \n alpha={3} \n beta={4}\n gamma={5}'.format(a, b, z, alpha, beta, gamma),
        bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
plt.legend(loc="upper center", prop={'size':18})



plt.show()