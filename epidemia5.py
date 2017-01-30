import matplotlib.pyplot as plt
import  numpy as np
from scipy.integrate import odeint

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'
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
# z - prawdopodobieństwo zgonu
# alpha - natularne urodzenia
# beta - natularne zgony
# gamma - działanie szczepionek



def uklad_rownan_bez_szczepienia(y, t, a, b, z, alpha, beta):
    P, N, W, M = y
    dP_dt = -a*N*P + alpha*(P + N + W)
    dN_dt = a*N*P - b*N - z*N
    dW_dt = b*N
    dM_dt = z*N + beta*(P + N + W)
    return dP_dt, dN_dt, dW_dt, dM_dt

def uklad_rownan_szczepienia_od_poczatku(y, t, a, b, z, alpha, beta, gamma):
    P, N, W, M = y
    dP_dt = -a * N * P + alpha * (P + N + W) - gamma * P
    dN_dt = a * N * P - b * N - z * N
    dW_dt = b * N + gamma * P
    dM_dt = z * N + beta * (P + N + W)
    return dP_dt, dN_dt, dW_dt, dM_dt


def uklad_rownan_szczepienia_zalezne_od_czasu(y, t, a, b, z, alpha, beta, gamma, t_poczatek, t_koniec):
    P, N, W, M = y
    dP_dt = -a * N * P + alpha * (P + N + W) - szczepienia(t, gamma, t_poczatek, t_koniec) * P
    dN_dt = a * N * P - b * N - z * N
    dW_dt = b * N + szczepienia(t, gamma, t_poczatek, t_koniec) * P
    dM_dt = z * N + beta * (P + N + W)
    return dP_dt, dN_dt, dW_dt, dM_dt

def szczepienia(t, gamma, t_poczatek, t_koniec):
    if t > t_poczatek and t < t_koniec:
        return gamma
    else:
        return 0


def symulacja_bez_szczepien_i_szczepienia_od_poczatku():
    # Warunki poczatkowe
    P_0 = 1000
    N_0 = 10
    W_0 = 0
    M_0 = 0

    a = 0.0005
    b = 1 / 10.0
    z = 0.05
    alpha = 0.002
    beta = 0.0001
    gamma = 0.05

    czas_w_dniach = np.linspace(0, 80, 1000)
    y_0 = P_0, N_0, W_0, M_0 # wektor warunków poczatkowych
    rozwiazanie = odeint(uklad_rownan_bez_szczepienia, y_0, czas_w_dniach, args=(a, b, z, alpha, beta))
    P, N, W, M = rozwiazanie.T

    # wykres dla przypadku bez szczepienia
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(121, axis_bgcolor='#dddddd', axisbelow=True)
    ax.plot(czas_w_dniach, P, 'b', alpha=0.5, lw=2, label="Podatni")
    ax.plot(czas_w_dniach, N, 'r', alpha=0.5, lw=2, label="Zarażeni")
    ax.plot(czas_w_dniach, W, 'g', alpha=0.5, lw=2, label="Uzdrowieni")
    ax.plot(czas_w_dniach, M, 'k', alpha=0.5, lw=2, label="Zgony")
    ax.set_ylim([0, 1350])
    ax.set_xlabel("Czas [dni]")
    ax.set_ylabel("Liczba osób")
    ax.set_title("Bez szczepienia")
    ax.text(50, 750, 'a={0}\nb={1} \nz={2} \n alpha={3} \n beta={4} \n P_0={5} \n N_0={6} \n W_0={7} \n M_0={8}'.format(
        a, b, z, alpha, beta, P_0, N_0, W_0, M_0), bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    plt.legend(loc="upper left", prop={'size':20})


    rozwiazanie_s = odeint(uklad_rownan_szczepienia_od_poczatku, y_0, czas_w_dniach, args=(a, b, z, alpha, beta, gamma))
    P_s, N_s, W_s, M_s = rozwiazanie_s.T
    ax2 = fig.add_subplot(122, axis_bgcolor='#dddddd', axisbelow=True)
    ax2.plot(czas_w_dniach, P_s, 'b', alpha=0.5, lw=2, label="Podatni")
    ax2.plot(czas_w_dniach, N_s, 'r', alpha=0.5, lw=2, label="Zarażeni")
    ax2.plot(czas_w_dniach, W_s, 'g', alpha=0.5, lw=2, label="Uzdrowieni")
    ax2.plot(czas_w_dniach, M_s, 'k', alpha=0.5, lw=2, label="Zgony")
    ax2.set_ylim([0, 1350])
    ax2.set_xlabel("Czas [dni]")
    ax2.set_ylabel("Liczba osób")
    ax2.set_title("szczepienie od początku")
    ax2.text(50, 400, 'a={0}\nb={1} \nz={2} \n alpha={3} \n beta={4} \n P_0={5} \n N_0={6} \n W_0={7} \n M_0={8}'.format(
        a, b, z, alpha, beta, P_0, N_0, W_0, M_0), bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    plt.legend(loc="upper center", prop={'size':20})
    plt.show()



def symulacja_bez_szczepien_i_szczepienia_zalezne_od_czasu():
    # Warunki poczatkowe
    P_0 = 1000
    N_0 = 10
    W_0 = 0
    M_0 = 0
    a = 0.0005
    b = 1 / 10.0
    z = 0.05
    alpha = 0.002
    beta = 0.0001
    gamma = 0.05
    czas_w_dniach = np.linspace(0, 80, 1000)
    y_0 = P_0, N_0, W_0, M_0 # wektor warunków poczatkowych


    poczatek_szczepienia_dzien = 1
    koniec_szczepienia_dzien = 40
    rozwiazanie_szczepienia_1_dnia = odeint(uklad_rownan_szczepienia_zalezne_od_czasu, y_0, czas_w_dniach,
                           args=(a, b, z, alpha, beta, gamma, poczatek_szczepienia_dzien, koniec_szczepienia_dzien))
    P, N, W, M = rozwiazanie_szczepienia_1_dnia.T

    # wykres dla przypadku bez szczepienia
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(121, axis_bgcolor='#dddddd', axisbelow=True)
    ax.plot(czas_w_dniach, P, 'b', alpha=0.5, lw=2, label="Podatni")
    ax.plot(czas_w_dniach, N, 'r', alpha=0.5, lw=2, label="Zarażeni")
    ax.plot(czas_w_dniach, W, 'g', alpha=0.5, lw=2, label="Uzdrowieni")
    ax.plot(czas_w_dniach, M, 'k', alpha=0.5, lw=2, label="Zgony")
    ax.set_ylim([0, 1250])
    ax.set_xlabel("Czas [dni]")
    ax.set_ylabel("Liczba osób")
    ax.set_title("szczepienia od 1-szego dnia do 40-tego dnia")
    ax.text(50, 450, 'a={0}\nb={1} \nz={2} \n alpha={3} \n beta={4} \n P_0={5} \n N_0={6} \n W_0={7} \n M_0={8}'.format(
        a, b, z, alpha, beta, P_0, N_0, W_0, M_0), bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    plt.legend(loc="upper center", prop={'size': 20})
    ax1 = ax.twinx()
    ax1.plot([1, 1, 40, 40], [0, 0.05, 0.05, 0], 'c-', lw=2)
    ax1.set_ylim([0, 0.5])
    ax1.set_ylabel("skutecznośc szczepionki", color='c')


    poczatek_szczepienia_dzien = 10
    koniec_szczepienia_dzien = 40
    rozwiazanie_od_10_dnia = odeint(uklad_rownan_szczepienia_zalezne_od_czasu, y_0, czas_w_dniach,
                           args=(a, b, z, alpha, beta, gamma, poczatek_szczepienia_dzien, koniec_szczepienia_dzien ))
    P_s, N_s, W_s, M_s = rozwiazanie_od_10_dnia.T
    ax2 = fig.add_subplot(122, axis_bgcolor='#dddddd', axisbelow=True)
    ax2.plot(czas_w_dniach, P_s, 'b', alpha=0.5, lw=2, label="Podatni")
    ax2.plot(czas_w_dniach, N_s, 'r', alpha=0.5, lw=2, label="Zarażeni")
    ax2.plot(czas_w_dniach, W_s, 'g', alpha=0.5, lw=2, label="Uzdrowieni")
    ax2.plot(czas_w_dniach, M_s, 'k', alpha=0.5, lw=2, label="Zgony")
    ax2.set_ylim([0, 1250])
    ax2.set_xlabel("Czas [dni]")
    ax2.set_ylabel("Liczba osób")
    ax2.set_title("szczepienie od 10-tego do 40-tego dnia")
    ax2.text(50, 400, 'a={0}\nb={1} \nz={2} \n alpha={3} \n beta={4} \n P_0={5} \n N_0={6} \n W_0={7} \n M_0={8}'.format(
        a, b, z, alpha, beta, P_0, N_0, W_0, M_0), bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    plt.legend(loc="upper center", prop={'size':20})

    ax3 = ax2.twinx()
    ax3.plot([10, 10, 40, 40], [0, 0.05, 0.05, 0], 'c-', lw=2)
    ax3.set_ylim([0, 0.5])
    ax3.set_ylabel("skutecznośc szczepionki", color='c')

    plt.subplots_adjust(left=0.08, right=0.93, top=0.93, bottom=0.1, hspace=0.29, wspace=0.320)
    plt.show()

def symulacja_bez_szczepienia_rozne_warunki_poczatkowe():
    # Warunki poczatkowe 1
    P_01 = 1000
    N_01 = 50
    W_01 = 0
    M_01 = 0

    a = 0.0005
    b = 1 / 10.0
    z = 0.05
    alpha = 0.002
    beta = 0.0001

    czas_w_dniach = np.linspace(0, 80, 1000)
    y_01 = P_01, N_01, W_01, M_01  # wektor warunków poczatkowych
    rozwiazanie_1 = odeint(uklad_rownan_bez_szczepienia, y_01, czas_w_dniach, args=(a, b, z, alpha, beta))
    P_1, N_1, W_1, M_1 = rozwiazanie_1.T

    # wykres dla przypadku bez szczepienia
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(121, axis_bgcolor='#dddddd', axisbelow=True)
    ax.plot(czas_w_dniach, P_1, 'b', alpha=0.5, lw=2, label="Podatni")
    ax.plot(czas_w_dniach, N_1, 'r', alpha=0.5, lw=2, label="Zarażeni")
    ax.plot(czas_w_dniach, W_1, 'g', alpha=0.5, lw=2, label="Uzdrowieni")
    ax.plot(czas_w_dniach, M_1, 'k', alpha=0.5, lw=2, label="Zgony")
    ax.set_ylim([0, 1350])
    ax.set_xlabel("Czas [dni]")
    ax.set_ylabel("Liczba osób")
    ax.set_title("Bez szczepienia")
    ax.text(50, 750, 'a={0}\nb={1} \nz={2} \n alpha={3} \n beta={4} \n P_0={5} \n N_0={6} \n W_0={7} \n M_0={8}'.format(
        a, b, z, alpha, beta, P_01, N_01, W_01, M_01), bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    plt.legend(loc="upper left", prop={'size': 20})

    # Warunki poczatkowe 1
    P_02 = 1000
    N_02 = 250
    W_02 = 0
    M_02 = 0

    y_02 = P_02, N_02, W_02, M_02  # wektor warunków poczatkowych
    rozwiazanie_2 = odeint(uklad_rownan_bez_szczepienia, y_02, czas_w_dniach, args=(a, b, z, alpha, beta))
    P_2, N_2, W_2, M_2 = rozwiazanie_2.T

    ax1 = fig.add_subplot(122, axis_bgcolor='#dddddd', axisbelow=True)
    ax1.plot(czas_w_dniach, P_2, 'b', alpha=0.5, lw=2, label="Podatni")
    ax1.plot(czas_w_dniach, N_2, 'r', alpha=0.5, lw=2, label="Zarażeni")
    ax1.plot(czas_w_dniach, W_2, 'g', alpha=0.5, lw=2, label="Uzdrowieni")
    ax1.plot(czas_w_dniach, M_2, 'k', alpha=0.5, lw=2, label="Zgony")
    ax1.set_ylim([0, 1350])
    ax1.set_xlabel("Czas [dni]")
    ax1.set_ylabel("Liczba osób")
    ax1.set_title("Bez szczepienia")
    ax1.text(50, 900, 'a={0}\nb={1} \nz={2} \n alpha={3} \n beta={4} \n P_0={5} \n N_0={6} \n W_0={7} \n M_0={8}'.format(
        a, b, z, alpha, beta, P_02, N_02, W_02, M_02), bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    plt.legend(loc="upper left", prop={'size': 20})

    plt.show()
