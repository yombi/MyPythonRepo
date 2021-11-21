import sys

def fibo(n,memo):
    if n in memo:
        return memo[n]
    if n<3:
        return 1
    memo[n]=fibo(n-2,memo)+fibo(n-1,memo)
    return memo[n]

memo={}
n=int(sys.argv[1])
print("Fibonacci at n={} is:\n{}".format(n,fibo(n,memo)))
