# -*- coding: utf-8 -*-
"""
Monolayer neural netweightork, created especially for embedded systems like arduino.

how to use:
network =  NeuralNetworkMonoLayer(num_input, num_class, p, t, epochs)
neuralNetwork = network.makeNetwork() ----> retur in a tupla Weight, bias and the error.

num_input ----> number of inputs to the neural network.
num_class ----> number of classes that is equal to the number of neurons.
p ----> patron
t ----> target
epochs ----> epochs XD


@author: Daniel Miranda Castillo ----> DMC0099
"""

import numpy as np

class NeuralNetworkMonoLayer():
    
    def __init__(self, num_input, num_class, p, t, epochs):
        self.num_input = num_input
        self.num_class = num_class
        self.p = p
        self.t = t
        self.epochs = epochs
        
    def makeNetwork(self):
        self.weight = 2 * np.random.rand(self.num_class,self.num_input) - 1
        self.weight = np.array(self.weight)
        self.bias = 2 * np.random.rand(self.num_class,1) - 1
        self.bias = np.array(self.bias)
        self.error = np.zeros((len(self.t), len(self.t[0])))
        
        for epoc in range(self.epochs):
            for self.q in range(len(self.p[0])):
                self.hardlin = self.function_hardlin()
                self.target = self.t[:,self.q]
                self.target = np.reshape(self.target, (self.num_class, 1))
                
                self.updateError()
                self.updateWeight()                
                self.updateBias()
                
        return self.weight , self.bias, self.error
    
    
    def function_hardlin(self):
        mul = (self.weight.dot(self.p[:,self.q]))
        mul = np.reshape(mul, (len(mul),1))
        suma = mul + self.bias
        hardlin = np.zeros((len(suma), len(suma[0])))
        for fil in range(len(suma)):
            for col in range(len(suma[0])):
                if(suma[fil, col] >= 0):
                    hardlin[fil, col] = 1
                else:
                    hardlin[fil, col] = 0
        return hardlin
        
    def updateError(self):
        resta = np.subtract(self.target, self.hardlin)
        resta = np.reshape(resta, (len(self.error), 1))
        for fil in range(len(resta)):
            for col in range(len(resta[0])):
                self.error[fil,self.q] = resta[fil,col]
    
    def updateWeight(self):
        patron = self.p[:,self.q]
        patron = np.reshape(patron,(len(self.p),1))
        error = self.error[:,self.q]
        error = np.reshape(error, (len(self.error), 1))
        self.weight = self.weight + error.dot(patron.T)
        
    def updateBias(self):
        error = self.error[:,self.q]
        error = np.reshape(error, (len(self.error), 1))
        self.bias = self.bias + error
        
    
    


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
        
network = NeuralNetworkMonoLayer(4, 3, p, t, 100)    
red = network.makeNetwork()

W = red[0]
b = red[1]
color = p[:,1]
color = np.reshape(color, (4,1))


n1 = ((W[0,0]*(color[0])) + (W[0,1]*(color[1]))+ (W[0,2]*(color[2])) + (W[0,3]*(color[3]))) + b[0];
n2 = ((W[1,0]*(color[0])) + (W[1,1]*(color[1]))+ (W[1,2]*(color[2])) + (W[1,3]*(color[3]))) + b[1];
n3 = ((W[2,0]*(color[0])) + (W[2,1]*(color[1]))+ (W[2,2]*(color[2])) + (W[2,3]*(color[3]))) + b[2];