# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 22:25:07 2021

@author: daniel Mirandacastillo
"""

import numpy as np

p = np.loadtxt("data.csv", delimiter=",")
p = p.T

t = np.zeros((3,60))

for i in range(60):
    if(i<=19):
        t[0,i] = 1
        t[1,i] = 0
        t[2,i] = 0
    if(i >= 20 and i <=39):
        t[0,i] = 0
        t[1,i] = 1
        t[2,i] = 0
    if(i>=40):
        t[0,i] = 0
        t[1,i] = 0
        t[2,i] = 1
        


def red_mono(num_para, num_clases, p, t, epocas):
    w = 2 * np.random.rand(num_clases,num_para) - 1
    w = np.array(w)
    b = 2 * np.random.rand(num_clases,1) - 1
    b = np.array(b)
    e = np.zeros((len(t), len(t[0])))
    
    for epoc in range(epocas):
        for q in range(len(p[0])):
            hardlin = fun_hardlin(w, p, b, q)
            target = t[:,q]
            target = np.reshape(target, (num_clases, 1))
            
            act_error(e, q, target, hardlin)
            
            act_W = act_w(w, e, p, q)
            w = act_W
            act_B = act_b(b, e, q)
            b = act_B
            
    return w , b, e


def fun_hardlin(w, p, b, q):
    mul = (w.dot(p[:,q]))
    mul = np.reshape(mul, (len(mul),1))
    suma = mul + b
    hardlin = np.zeros((len(suma), len(suma[0])))
    for fil in range(len(suma)):
        for col in range(len(suma[0])):
            if(suma[fil, col] >= 0):
                hardlin[fil, col] = 1
            else:
                hardlin[fil, col] = 0
    return hardlin
    
def act_error(e, q, target, hardlin):
    resta = np.subtract(target, hardlin)
    resta = np.reshape(resta, (len(e), 1))
    for fil in range(len(resta)):
        for col in range(len(resta[0])):
            e[fil,q] = resta[fil,col]

def act_w(w, e, p, q):
    patron = p[:,q]
    patron = np.reshape(patron,(len(p),1))
    error = e[:,q]
    error = np.reshape(error, (len(e), 1))
    w = w + error.dot(patron.T)
    return w
    
def act_b(b, e, q):
    error = e[:,q]
    error = np.reshape(error, (len(e), 1))
    b = b + error
    return b
    
    


red = red_mono(4, 3, p, t, 100)


W = red[0]
b = red[1]
color = p[:,1]
color = np.reshape(color, (4,1))


n1 = ((W[0,0]*(color[0])) + (W[0,1]*(color[1]))+ (W[0,2]*(color[2])) + (W[0,3]*(color[3]))) + b[0];
n2 = ((W[1,0]*(color[0])) + (W[1,1]*(color[1]))+ (W[1,2]*(color[2])) + (W[1,3]*(color[3]))) + b[1];
n3 = ((W[2,0]*(color[0])) + (W[2,1]*(color[1]))+ (W[2,2]*(color[2])) + (W[2,3]*(color[3]))) + b[2];