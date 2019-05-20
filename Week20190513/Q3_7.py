#!/usr/bin/env python3
import numpy as np

theta = 0.3
print("Theta: {}".format(theta))
years = 6
r00 = 0.05
print("r00: {}".format(r00))
print("r0n factor: 0.9")
t=6
r0n = [r00]

#Array of interest rates
for i in range(1, t+1):
    r0n.append(r0n[i-1]*0.9)

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
            if r_t[i][j]>0.06:
                treecolumn.append(100000*(r_t[i][j]-0.06))
            if r_t[i][j]<=0.06:
                treecolumn.append(0)
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


cash_flows = cf_tree(5)
present_value = pv_tree(r_t,cash_flows)

print("5 year cash flow tree")
print(cash_flows)
print("5 year PV tree")
print(present_value)
print()
print("Present value of bond: ${0:.2f}".format(present_value[0][0]))
