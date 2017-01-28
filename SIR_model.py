import matplotlib.pyplot as plt
import  numpy as np
from scipy.integrate import odeint

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.unicode'] = True
plt.rcParams.update({'font.size': 22})
plt.rcParams['text.latex.preamble'] = r'\usepackage[T1]{polski}'



# N - populacja
# S - podatni, którzy nie są jeszcze chodzy
# I - zakażeni
# R - uzdrowieni, nie są już podatni


N = 1000
I_0, R_0 = 1,0 # Warunki początkowe: liczba zakażonych, liczba wyzdrowiałych
S_0 = N - I_0 - R_0
czas_w_dniach = np.linspace(0, 160, 1000)
beta = 0.2      #prawdopodobieństwa zarażenia przy kontakcie
gamma = 1./10   #średni czas dochodzenia do zdrowia 1/dzień


def uklad_rownan(y, t, N, beta, gamma):
    S, I, R = y
    dS_dt = (-beta * S * I) / N
    dI_dt = (beta * S *  I) / N - gamma*I
    dR_dt = gamma*I
    return dS_dt, dI_dt, dR_dt

y_0 = S_0, I_0, R_0

rozwiazanie = odeint(uklad_rownan, y_0, czas_w_dniach, args=(N, beta, gamma))
S, I, R = rozwiazanie.T

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axis_bgcolor='#dddddd', axisbelow=True)
ax.plot(czas_w_dniach, S, 'b', alpha=0.5, lw=2, label="Podatni")
ax.plot(czas_w_dniach, I, 'r', alpha=0.5, lw=2, label="Zarażeni")
ax.plot(czas_w_dniach, R, 'g', alpha=0.5, lw=2, label="Uzdrowieni")
ax.set_xlabel("Czas [dni]")
ax.set_ylabel("Liczba osób")
plt.legend(loc="center right")
plt.show()
