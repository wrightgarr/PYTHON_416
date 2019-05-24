#!/usr/bin/env python3
import numpy as np
import scipy.optimize as spo

#theta for the question
given_theta = 0.3
#array of target spot rates
target_spot_rates= np.array([0.0249,0.0250,0.0233,0.0245,0.0247,0.0250,0.0254,0.0257,0.0262,0.0265])
#array of rzero guesses
rzero = np.array([0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01])
years = 10
#r00 = 0.05
t=10

def fillratetree(r0,theta):
    ratetree=[]
    for i,element in enumerate(r0):
        treecolumn=[]
        for j in range(0,i+1):
            apnd = element*np.exp(2*j*theta)
            treecolumn.append(apnd)
        ratetree.append(treecolumn)
    return ratetree

#Cash Flow tree
def cf_tree(t):
    cftree=[]
    for i in range(0, t+1):
        treecolumn=[]
        for j in range(0,i+1):
            if i < t:
                treecolumn.append(0)
            if i == t:
                treecolumn.append(100)
        cftree.append(treecolumn)
    return cftree

#Present value tree
def comppvtree(ratetree,cvtree):
    pvtree=[]
    for element in cvtree:
        parttree=[]
        for element2 in element:
            parttree.append(0)
        pvtree.append(parttree)
    icol=len(pvtree)-1
    for j in range(0,icol+1):
        pvtree[icol][j]=cvtree[icol][j]   
    for i in range (1,len(pvtree)):
        icol=len(pvtree)-1-i
        for j in range(0,icol+1):
            pvtree[icol][j]=cvtree[icol][j]+(0.5*pvtree[icol+1][j+1]+0.5*pvtree[icol+1][j])/(1+ratetree[icol][j])
    return pvtree

#Spot Rates
def spotrates(r0):
    spot_array = []
    for i in range(1,t+1):
        pv = comppvtree(fillratetree(r0,given_theta),cf_tree(i))[0][0]
        spot_rate = (100/pv)**(1/i)-1
        spot_array.append(spot_rate)
    return spot_array

def to_min(r0,theta,target):
    return np.sum(np.square((spotrates(r0)) - target))*1000000000


result = spo.minimize(to_min,[rzero],(given_theta,target_spot_rates,),method='SLSQP',options={'disp':True})
answer = result.x
print()
print("The list of r0n rates that minimise the difference between spot rates:")
print(answer)
print()
print("Target Spot Rates from WSJ:")
print(target_spot_rates)
print("Spotrates from model:")
print(spotrates(answer))


