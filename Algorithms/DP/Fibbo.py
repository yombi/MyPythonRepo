import sys

def fibo(n,memo):
    #We have already calculated the n possition of fibbonacci
    if n in memo:
        return memo[n]
    #Base case needed in recursion
    if n<3:
        return 1
    #Dinamic Programing: return the sum of the 2 previous possitions(by using fibo function) and save it. This is gonna return 1 for the first two possitions
    memo[n]=fibo(n-2,memo)+fibo(n-1,memo)
    #Return the list with the fibbonacci serie
    return memo[n]
#Defining dictionary
memo={}
#Parsing argument from command line
n=int(sys.argv[1])
print("Fibonacci at n={} is:\n{}".format(n,fibo(n,memo)))
