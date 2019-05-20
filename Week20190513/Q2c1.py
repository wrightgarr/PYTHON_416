#!/usr/bin/env python3
import numpy as np

theta = 0.2
print("Theta: {}".format(theta))
years = 6
r00 = 0.05
print("r00: {}".format(r00))
print("r0n factor: 0.8")
t=6
r0n = [r00]

#Array of interest rates
for i in range(1, t+1):
    r0n.append(r0n[i-1]*0.8)

#Interest rate tree using array and volatility parameter
def rate_tree(r0n,theta):
    ratetree=[]
    for i,element in enumerate(r0n):
        treecolumn=[]
        for j in range(0,i+1):
            treecolumn.append(element*np.exp(2*j*theta))
        ratetree.append(treecolumn)
    return ratetree

#Interest rate tree
r_t = rate_tree(r0n, theta)

#Cashflow tree using only number of period parameter
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
def pv_tree(ratetree,cftree):
    pvtree=[]
    for element in cftree:
        parttree=[]
        for element2 in element:
            parttree.append(0)
        pvtree.append(parttree)
    icol=len(pvtree)-1
    for j in range(0,icol+1):    
        pvtree[icol][j]=cftree[icol][j]   
    for i in range (1,len(pvtree)):
        icol=len(pvtree)-1-i   
        for j in range(0,icol+1):
            pvtree[icol][j]=cftree[icol][j]+(0.5*pvtree[icol+1][j+1]+0.5*pvtree[icol+1][j])/(1+ratetree[icol][j])
    return pvtree

#Define function to calculate spot rates
def sr(pv,periods):
    return (100/pv)**(1/periods)-1

#Create an array with the PV trees for bonds of different durations
pv_array_tree = []
#and the spot rates
spot_array = []
for i in range(1,t+1):
    present_value_tree = pv_tree(rate_tree(r0n, theta),cf_tree(i))
    pv_array_tree.append(present_value_tree)
    spot_rate = sr(pv_array_tree[i-1][0][0],i)
    spot_array.append(spot_rate)

#Calculating forward rates
forward_array = [spot_array[0]]
for i in range(1,t):
    forward_array.append((1+spot_array[i])**(i+1)/(1+spot_array[i-1])**(i)-1)

print()
print("BDT Lattice Rate Tree")
print(r_t)
print()
print("Spot Rates")
print(spot_array)
print()
print("Forward Array")
print(forward_array)









