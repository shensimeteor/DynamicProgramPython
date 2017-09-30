#!/usr/bin/env python
#implement: a. brute force solving TSP; b. DP (bottom_up) solving TSP, use a to verif b, test passed
#what impress me most is DP (though exponential) still much less than n! brute-force algorithm
import math
import numpy as np
import time

#C[n+1][n+1], for 1..n, calc the min path (0->i1->i2->..->in->0)
#brute force algorithm------------------------------
#return (cost, optimal_path)
def tsp_brute_force(C):
    n=len(C)-1
    path_all=get_permutation_recursive(n)
    min_cost=float('inf')
    for path in path_all:
        cost=C[0][path[0]] + C[path[n-1]][0]
        for k in range(n-1):
            cost=cost+C[path[k]][path[k+1]]
        if(min_cost > cost):
            min_cost=cost
            min_path=path
    return((min_cost, min_path))

#output 2-dim list, i.e., all permutations given 1,2..,n
def get_permutation_recursive(n):
    if(n == 1):
        return [[1]]
    else:
        lst=get_permutation_recursive(n-1)
        n_lst=len(lst)
        nfact=math.factorial(n)
        newlst=[[0 for i in range(n)] for j in range(nfact)]
        temp=[0 for i in range(n)]
        cnt=0
        for i in range(n):
            for j in range(n_lst):
                newlst[cnt][0:i]= lst[j][0:i]
                newlst[cnt][i] = n
                newlst[cnt][i+1:n] = lst[j][i:n-1]
                cnt+=1
        return newlst
 
#Dynamic Programming ----------------------
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

#given code (representing a list), minus the idx vertex
def code_combination_setminus(code, idx):
    idx_code=encode_combination([idx])
    if (idx_code & code > 0):
        code = code - idx_code
    return (code)

#return (cost, opt_path)
def tsp_dp_bottom_up(C):
    n=len(C)-1
    n_comb=1<<n
    M=np.zeros((n+1,n_comb)) 
    #M[v][w] save the min-cost for (v--starting vertex, set--a set of vertex to go thourgh before 0,
    #i.e. v->{set}->0. set is presented by a int number w
    S=np.zeros((n+1,n_comb),dtype=np.int)
    #S[v][w] save the successor of v in the set presented by int number w, in optimal path
    lst_vertex_visit=[i for i in range(0,n+1)]
    for w in range(0, n_comb):
        for v in lst_vertex_visit:
            if w==0:
                M[v][w]=C[v][0]
                S[v][w]=0
            else:
                w_lst=decode_combination(w)
                if v in w_lst:
                    continue
                min_cost=float('inf')
                for z in w_lst:
                    code_rest=code_combination_setminus(w, z)
                    cost=C[v][z] + M[z][code_rest]
                    if(cost < min_cost):
                        min_cost=cost
                        S[v][w]=z
                M[v][w]=min_cost
    #final min cost
    min_cost = M[0][n_comb-1]
    #costruct opt-path
    opt_path=[0]
    opt_path.append(S[0][n_comb-1])
    last=S[0][n_comb-1]
    w=n_comb-1
    while w>0:
        w=code_combination_setminus(w, last)
        opt_path.append(S[last][w])
        last=S[last][w]
    return((min_cost, opt_path))
    

    
if __name__ == "__main__":
# test all_permutation    
#    all_permutation=get_permutation_recursive(5)
#    print(len(all_permutation))
#    all_permutation_tuple=[tuple(x) for x in all_permutation]
#    print(len(set(all_permutation_tuple)))
# test tsp_brute_force
    #C=[[0,1,3,2,6], [1,0,1,2,2], [1,1,0,3,4], [2,2,3,0,5]]
# use random C matrix
    n_city=4
    n_add0=n_city+1
    C=np.random.randint(low=1, high=7, size=(n_add0, n_add0))
    C[range(n_city+1), range(n_city+1)] = 0
    print(C)
    start=time.clock()
    for i in range(1):
        (min_cost, opt_path)=tsp_brute_force(C)
    print("brute force: second of "+str(time.clock()- start))
    print(opt_path)
    print(min_cost)
# test tsp_dp_bottom_up
    start=time.clock()
    for i in range(1):
        (min_cost, opt_path)=tsp_dp_bottom_up(C)
    print("np bottom-up: second of "+str(time.clock()- start))
    print(opt_path)
    print(min_cost)

