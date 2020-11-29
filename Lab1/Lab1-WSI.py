from sympy import *
import numpy as np
import random

def getJx(b,A):
    x = []
    jx = 0

    # Tworzę tablice o ilości elementów równej wymiarowi b w postaci [x1, x2, x3, ... , xn]
    for symbol in symbols(f'x:{b.shape[0]}'):
        x.append(symbol)
    x = np.array(x)

    # Obliczam J(x) według wzoru
    func = x.dot(np.transpose([b])) + 0.5*x.dot((A.dot(np.transpose(x))))
    for a in func:
        jx += a
    return jx, x

def calculateGradient(Jx, X, P):
    gradient = []
    point = {}

    # Tworzenie tablicy, której elementy są w postaci xn : punkt[n]
    for i in range(P.shape[0]):
        point.update({X[i]:P[i]})

    # Każdy element tablicy gradient jest pochodną po odpowiadającym jego miejscu xn
    for symbol in X:
        gradient.append((diff(Jx, symbol)))

    # Zamieniam każdy element tablicy gradient na wartość pochodnej w tym punkcie
    for i in range(len(gradient)):
        gradient[i] = gradient[i].subs(point).evalf()
    gradient = np.array(gradient)

    return gradient

def checkPositivity(A):
    for i in range(1,A.shape[0]+1):
        if np.linalg.det(A[:i, :i]) <= 0:
            return False
    return True

def NewtonsMethod(Jx, X, hess):
    if not checkPositivity(hess):
        return None
    x = np.zeros(len(X),)
    return x - np.linalg.inv(hess).dot(calculateGradient(Jx, X, x))

def gradientsMethod(Jx, X, hess, beta=0.5, steps=1500):
    if not checkPositivity(hess):
        return None
    x = np.zeros(len(X),)
    while(steps > 0):
        x = x - beta*calculateGradient(Jx, X, x)
        steps-=1
    return x

def sghMethod(b, A, X):
    m = X.shape[0]*(X.shape[0]+1)
    summands = []
    x = np.zeros(len(X),)

    for i in range(0,X.shape[0]):
        summands.append(m*X[i]*b[i])
    
    for i in range(0,X.shape[0]):
        for j in range(0,X.shape[0]):
            summands.append(m*0.5*(X[i]*X[j])*A[i,j])

    a = random.randint(0,len(summands)-1)

    steps = 1
    while(steps < 2000):
        beta = 2/(100+steps)
        a = random.randint(0,len(summands)-1)
        x = x - beta*calculateGradient(summands[a], X, x)
        steps+=1

    return x


def main():
    b = []
    A = []
    print("------------------------------------------------------------------")
    print("J(x) = b^T * x + 0.5 * x^T * A * x")
    print("Program minimalizujący funkcję J(x) trzema metodami: ")
    print("- Newtona")
    print("- gradientu prostego")
    print("- stochastycznego najszybszego spadku")
    print("Opcje do wyboru:")
    print("1. Wprowadzenie danych samodzielnie")
    print("2. Program sam losuje macierz A i wektor b w podanym wymiarze przestrzeni")
    x = int(input("Wybierz opcje: "))

    if x == 1:
        print("------------------------------------------------------------------")
        d = int(input("Podaj wymiar przesrzeni: "))
        for i in range(1,d+1):
            b.append(float((input(f'Podaj {i} współrzędną wektora b: '))))
        b = np.array(b)
        print("------------------------------------------------------------------")
        for i in range(1,d+1):
            row = []
            for j in range(1,d+1):
                row.append(float((input(f'Podaj {j} współrzędną {i} wiersza macierzy A: '))))
            A.append(row)
        A = np.array(A)
        print("------------------------------------------------------------------")
        if not checkPositivity(A):
            print("Macierz A nie jest dodatnio określona.")
            x = input("Wciśnij \"ENTER\" żeby opuścić program")
            return None

    elif x == 2:
        d = int(input("Podaj wymiar przesrzeni: "))
        A = np.random.random((d,d))
        while np.linalg.det(A) == 0:
            A = np.random.random((d,d))
        A = A.dot(np.transpose(A))
        b = np.random.random((d,))

    print("Wektor b: ", end="")
    print(b)
    print("Macierz A: ",end="")
    print(A)
    print("------------------------------------------------------------------")
    print("Minimalna wartość funkcji znaleziona metodą Newtona: ", end="")
    print(NewtonsMethod(getJx(b,A)[0], getJx(b,A)[1], A))
    print("Minimalna wartość funkcji znaleziona metodą gradientu prostego: ", end="")
    print(gradientsMethod(getJx(b,A)[0], getJx(b,A)[1], A))
    print("Minimalna wartość funkcji znaleziona metodą stochastycznego najszybszego spadku: ", end="")
    print(sghMethod(b, A, getJx(b,A)[1]))


def tests():
    # Przykładowe dane dla 2 wymiarów
    b = np.array([2,2])
    A = np.array([[2,1], [1,3]])

    # Przykładowe dane dla 2 wymiarów
    b1 = np.array([-1,2,-3])
    A1 = np.array([[3,1,-1],[1,1,0],[-1,0,2]])

    print("Wektor b: ", end="")
    print(b)
    print("Macierz A: ",end="")
    print(A)
    print("------------------------------------------------------------------")
    print("Minimalna wartość funkcji znaleziona metodą Newtona: ", end="")
    print(NewtonsMethod(getJx(b,A)[0], getJx(b,A)[1], A))
    print("Minimalna wartość funkcji znaleziona metodą gradientu prostego: ", end="")
    print(gradientsMethod(getJx(b,A)[0], getJx(b,A)[1], A))
    print("Minimalna wartość funkcji znaleziona metodą stochastycznego najszybszego spadku: ", end="")
    print(sghMethod(b, A, getJx(b,A)[1]))

    print("Wektor b: ", end="")
    print(b1)
    print("Macierz A: ",end="")
    print(A1)
    print("------------------------------------------------------------------")
    print("Minimalna wartość funkcji znaleziona metodą Newtona: ", end="")
    print(NewtonsMethod(getJx(b1,A1)[0], getJx(b1,A1)[1], A1))
    print("Minimalna wartość funkcji znaleziona metodą gradientu prostego: ", end="")
    print(gradientsMethod(getJx(b1,A1)[0], getJx(b1,A1)[1], A1))
    print("Minimalna wartość funkcji znaleziona metodą stochastycznego najszybszego spadku: ", end="")
    print(sghMethod(b1, A1, getJx(b1,A1)[1]))


tests()

