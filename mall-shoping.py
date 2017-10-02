#!/usr/bin/env python

import itertools
import time
import numpy as np

#v_array(n), d_matrix(n+1,n+1)
def solve_brute_force(v_array, d_matrix):
    n=len(v_array)
    id=[i+1 for i in range(n)]
    #get all perms_list (P(n,1) + P(n,2)+ P(n,3) + ..)
    perms_list=[]
    for i in range(n):
        lst_perm=list(itertools.permutations(id, i+1))
        perms_list.extend(lst_perm)
    #search for every perm in perms_list
    max_reward=float("-inf")
    for perm in perms_list:
        reward=sum([ v_array[x-1] for x in perm ]) - d_matrix[0][perm[0]] - d_matrix[perm[-1]][0]
        len_perm=len(perm)
        for i in range(len_perm-1):
            reward = reward - d_matrix[perm[i]][perm[i+1]]
        if reward > max_reward:
            max_reward = reward
            opt_path=perm
        #print(str(perm) + "  "+str(reward))
    return (max_reward, opt_path)

#
#combination (list) to int ( list size should be less than 30)
def encode_combination(lst_vertex):
    code=0
    for v in lst_vertex:
        code=code+1<< (v-1)
    return(code)

#from code, return sorted list containing vertex
def decode_combination(code):
    lst=list()
    cnt=0
    while (code > 0):
        cnt+=1
        if(code % 2 > 0):
            lst.append(cnt)
        code = code >> 1
    return lst

#return true if idx is contained in the list represente by code, else false
def code_combination_contain(code, idx):
    idx_code=encode_combination([idx])
    return bool(idx_code & code)

#given code (representing a list), minus the idx vertex
def code_combination_setminus(code, idx):
    idx_code=encode_combination([idx])
    if (idx_code & code > 0):
        code = code - idx_code
    return (code)

def solve_dp_bottom_up(v_array, d_matrix):
    n=len(v_array)
    vnew=[0]
    vnew.extend(v_array) #now change to n+1 dim 0(home) value: 0
    n_comb = 1<<n
    M=np.zeros((n+1,n_comb))
    S=np.zeros((n+1,n_comb), np.int) #successor of j vertex through subset of i vertex set
    for i in range(n_comb):
        for j in range(n+1):
            if i == 0:
                M[j][i] = vnew[j] - d_matrix[j][0]
                S[j][i] = 0
            else:
                if(j!=0 and code_combination_contain(i, j)):
                    M[j][i]=float("inf")
                    continue
                max_reward=vnew[j] - d_matrix[j][0]
                S[j][i]=0
                i_lst=decode_combination(i)
                for z in i_lst:
                    reward = vnew[j] - d_matrix[j][z] + M[z][code_combination_setminus(i, z)] 
                    if (reward > max_reward): 
                        max_reward = reward
                        S[j][i] = z
                M[j][i] = max_reward
    #construct path
    print("to construct path")
    path=[0]
    last=S[0][n_comb-1]
    path.append(S[0][n_comb-1])
    setcode=code_combination_setminus(n_comb-1, last)
    while last > 0:
        path.append(S[last][setcode])
        last=S[last][setcode]
        setcode=code_combination_setminus(setcode, last)
    return( M[0][n_comb-1], path)
     

    
if __name__ == "__main__":
    
    n_mall=4
    v_array=np.random.randint(low=3, high=7, size=(n_mall))
    d_matrix=np.random.randint(low=1, high=9, size=(n_mall+1, n_mall+1))
    d_matrix[range(n_mall+1), range(n_mall+1)] = 0  
    print(v_array)
    print(d_matrix)
    print("brute force")
    start=time.clock()
    (max_reward, opt_path) = solve_brute_force(v_array, d_matrix)
    print("seconds: "+str(time.clock() - start))
    print(max_reward)
    print(opt_path)
    print("dp bottom_up")
    start=time.clock()
    (max_reward, opt_path) = solve_dp_bottom_up(v_array, d_matrix)
    print(max_reward)
    print(opt_path)
    print("seconds: "+str(time.clock() - start))
    

