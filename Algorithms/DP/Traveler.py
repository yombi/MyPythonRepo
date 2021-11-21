import sys

def travel(n,m,memo):
    if n*m==0:
        return 0
    if n==1 or m==1:
        return 1
    if (n,m) in memo or (m,n) in memo:
        return memo[(n,m)]
    memo[(n,m)]=travel(n-1,m,memo)+travel(n,m-1,memo)
    memo[(m,n)]=travel(n-1,m,memo)+travel(n,m-1,memo)
    return memo[(n,m)]

memo={}
n=int(sys.argv[1])
m=int(sys.argv[2])
print("For a grid of {}*{} the answer is:\n{}".format(n,m,travel(n,m,memo)))
