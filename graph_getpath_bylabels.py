#!/usr/bin/env python
import copy
import math
import numpy as np

#C_matrix: 0 .. n-1, start_vertex: id starting with 0
#return (YES|NO, <path_list[[]]|NO found>
def get_path_bylabel_DP(C_matrix, label_list, start_vertex):
    n=len(C_matrix)
    k=len(label_list)
    P=np.zeros((n,k+1), np.object)
    #P[j][i] means: if a path starting with vertex-j & go through S[i] labels 
    # can be found, then P[j][i] = next vertex-id after j (can be multiple, use , to seprate)
    # e.g. P[j][i] = "2,5" means, 2,5 vertex can be after j to have such path
    # else (no such path), P[j][i] = "NO"
    for i in range(k+1):
        #S[i] = <o(k-i+1) .. o(k)>
        for j in range(n):
            P[j,i]=""
            if(i == 0):
                P[j,i]="end"
            else:
                for iw in range(n):
                    if P[iw,i-1] != "NO" and C_matrix[j,iw] == label_list[k-i]:
                        P[j,i] = P[j,i]+","+str(iw)
                if not P[j,i]:
                    P[j,i] = "NO"
            P[j,i]=P[j,i].strip(",")
    print(P)
    #construct path by P matrix
    if(P[start_vertex][k] == "NO"):
        ans="NO"
        path_list=[]
    else:
        ans="YES"
        path_list=construct_path_recursive(P, start_vertex, k)
    return((ans, path_list))

#return path list
def construct_path_recursive(P_matrix, i, j):
    path_list=[]
    head=[i]
    item=P_matrix[i][j]
    if(item == "end"):
        return([[i]])
    if(item == "NO"):
        exit(1)
    child_path_list=[]
    for v in item.split(','):
        v_path_list=construct_path_recursive(P_matrix, int(v), j-1)
        child_path_list.extend(v_path_list)
    for childpath in child_path_list:
        headx=copy.copy(head)
        headx.extend(childpath)
        path_list.append(headx)
    return(path_list)


if __name__ == "__main__":
    n=3
#    C=np.zeros((n,n), np.int)
    C=np.array([[0,1,1], [1,0,2], [3,2,0]])
    print(C)
    obs_label=[1,2,3]
    (ans, path_list) = get_path_bylabel_DP(C, obs_label, int(0))
    print(ans)
    print(path_list)


   



