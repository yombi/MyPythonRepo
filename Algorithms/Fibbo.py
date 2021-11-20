import sys

def fibo(n,dict):
    if n in dict:
        return dict[n]
    if n<3:
        return 1
    dict[n]=fibo(n-2,dict)+fibo(n-1,dict)
    return dict[n]

dict={}
n=int(sys.argv[1])
print("Fibonacci at n={} is:\n{}".format(n,fibo(n,dict)))
