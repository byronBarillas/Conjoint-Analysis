## Module containing linear algebra functions.
#It relies on just python language without packages like numpy etc.

#####################################################################################
def transpose(A): # This function finds the transpose of any size matrix (no vectors)
    n = len(A)
    m = len(A[0])
    exec('B = '+'['+'[],'*m+']')     
    for i in range(m):        
        for j in range(n):
            B[i].append(A[j][i])        
    return B

##############################################################################################
def matmat(A,B): # This function multiplies two matrices of any size which conform (no vectors)
    n = len(A)
    m = len(A[0])
    r = len(B)
    t = len(B[0])

    if m != r:
        return 'Error; matrices do not conform'

    exec('C = '+'['+'[],'*n+']')

    for i in range(n):        
        for j in range(t):
            c = 0
            for k in range(r):
                c = c + A[i][k]*B[k][j]
                
            C[i].append(c)
    return C
###################################################################################################
def matvec(A,b): # This function multiplies a matrix and a vector. It treats b as an upright vector 
    n = len(A)
    m = len(A[0])
    blen = len(b)

    y = []
    if m != blen:
        return 'Error; matrix and vector do not conform'
    for i in range(n):
        c = 0
        for j in range(m):
            c = c+A[i][j]*b[j]
        y.append(c)
    return y        

######################################################################################################################################
def solver(A,b): # This function solves the equation Ax = b using Gaussian elimination with partial pivoting and backward substitution
    n = len(A)
    m = len(A[0])
    blen = len(b)
    if n != m:
        return 'Error; Matrix is not square'
    if n != blen:
        return 'Error; Matrix and vector not of appriate size'
    # Solving using Gaussian Elimination with Partial Pivoting

    for i in range(n):
        a = []
        for j in range(i,n):  #Pivoting stage finds max entry in ith column and swaps its row with pivot row
            a.append(abs(A[j][i]))
        
        maxi = max(a)
        pos = a.index(maxi)

        if pos != 0:
            Ai = A[i]
            bi = b[i]
            Ak = A[i+pos]
            bk = b[i+pos]
            A[i] = Ak
            b[i] = bk
            A[i+pos] = Ai
            b[i+pos] = bi

        for j in range(i+1,n): #Gaussian Elimination stage
            if abs(A[i][i]) < 0.00000005:
                return 'matrix is singular to reasonable precision: \nThis would indicate that at least one variable is perfectly predictable from the others'
            mij = A[j][i]/A[i][i]

            for k in range(n):
                A[j][k] = A[j][k] - A[i][k]*mij
            b[j] = b[j] - b[i]*mij
    x = [0]*(n)
    x[n-1] = b[n-1]/A[n-1][n-1]
    
    nb = range(n-1)
    nb.reverse()

    for i in nb:          #Backward Substitution stage
        
        s = 0
        nbj = range(n-i-1)
        for j in nbj:
            s = s + A[i][n-1-j]*x[n-1-j]
        x[i]=((b[i]-s)/A[i][i])
        

    return x
    



