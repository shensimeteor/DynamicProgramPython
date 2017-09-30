#!/usr/bin/env python

comb=[]

def get_num_combination(arr_cent, n_cents, rec_matx):
    m=len(arr_cent)
    n=n_cents
    if(rec_matx[m][n] >= 0):
        return rec_matx[m][n]
    if(n==0):
        rec_matx[m][n]=1
    elif (m==0):
        rec_matx[m][n]=0
    else:
        k=n_cents//arr_cent[m-1]
        rec_matx[m][n]=get_num_combination(arr_cent[0:m-1], n, rec_matx)
        for i in range(1,k+1):
            if( n >= i*arr_cent[m-1] ):
                rec_matx[m][n] += get_num_combination(arr_cent[0:m-1], n-i*arr_cent[m-1], rec_matx)
    return(rec_matx[m][n])


if __name__ == "__main__":
    arr_cent=[1,2,5]
    n_cents=100
    rec_matx=[[-1 for i in range(0,n_cents+1)] for j in range(0,4+1)]
    print(rec_matx)
    n_comb=get_num_combination(arr_cent, n_cents, rec_matx)
    print(n_comb)
    print(rec_matx)
        






        

    

