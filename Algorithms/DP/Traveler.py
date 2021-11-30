import sys

def travel(n,m,memo):
    #Base case: n or m are zero
    if n*m==0:
        return 0
    #Base case: We have a grid with one row or one column
    if n==1 or m==1:
        return 1
    #If we have calculated the solution to a grid of n*m before, just return it
    #Note that the solution to a grid of n*m is the same as one of m*n
    if (n,m) in memo or (m,n) in memo:
        return memo[(n,m)]
    #Dinamic Programing: The arguments of travel() simulate a step taken to the right or down
    memo[(n,m)]=travel(n-1,m,memo)+travel(n,m-1,memo)
    memo[(m,n)]=travel(n-1,m,memo)+travel(n,m-1,memo)
    #Return the dictonary with all the solutions to different calculated grids
    return memo[(n,m)]

#Define dictonary
memo={}
#Parsing argument from command line
n=int(sys.argv[1])
m=int(sys.argv[2])
print("For a grid of {}*{} the answer is:\n{}".format(n,m,travel(n,m,memo)))
