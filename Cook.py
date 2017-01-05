import LinearAlgebra, math

####################################################################################
# This function makes the configuration binary code into dummy variable binary code

# Input -> RawData1 is a CSV, with NO EMPTY TRAILING ENTRIES. Each row represents the different configurations
#          The last row (FC) of this file should contain the number in each category at the end entry of each
#          category
# Output -> Data1: Dummy variable version of binary format feature data
#           FC: which contains the dummy variable attribute category widths
#           
# m = number of attribute configurations
# READ FILE AND ASSIGN TO Data1 list of lists which contain string elements 
# Each list inside Data1 corresponds to the rows of the CSV file
###########################################################################
def DummyConvert():

    datafile1 = open('RawData1.CSV','r')

    Data = datafile1.readlines()
    Data01 = []
    datafile1.close()

    for line in Data:
        Data01.append(line.split(','))

    del Data
# Make array with (0,1) corresponding to presence or not of a feature value

    m = len(Data01)-2
    mval = len(Data01[0])

    Attributes = Data01[0] # Contains the names of the attributes
    FC = Data01[-1]        # Contains the attribute category length information
    del FC[0]
    del Data01[0], Data01[-1]


    rows = range(m)
    columns = range(mval)
    del columns[0]


    exec('Data1 = '+'['+'[],'*m+']')

# Loop creates ordered attribute value data
    L = []
    for line in rows:
        for charz in columns:
            L.append(eval(Data01[line][charz]))
        Data1[line] = L
        L = []

# Make a list with the widths of the attribute categories
    FC1 = []
    for e in range(len(FC)):
        if FC[e] != '':
            FC1.append(eval(FC[e]))
    FC = FC1
    del FC1


# Erase first attribute of each category; -----{could have made another Data01 that takes only dummy vars from Data1}-------------------------------------------------------------------------------------------------

    lenFC = len(FC)

    for i in range(m):
        c = 0
        c1 = 0
        for j in range(len(FC)):
            del Data1[i][c-c1]
            c1 = c1 + 1
            c = c + FC[j]



# Modify FC to conform to dummy variable widths

    for i in range(len(FC)):
        FC[i] = FC[i]-1


    return [Data1,FC,Attributes]
##########################################################################################################
# This function transforms best features to highest number
# Input -> RawData2. RawData2 is a CSV, with no empty trailing entries, file in which every row represents
# a respondents preference order from most prefered 1, to least prefered. 
# Output -> Data2. List of lists of respondent data. The rows correspond to
# to individual subject preferences

# n = number of subjects/respondents in the study (height of collumns)
# nsub = number of attribute confugurations 
####################################################################################################



#READ FILE AND ASSIGN TO Data2 list of lists which contain string elements ---------------------------------
# Each list inside Data2 corresponds to the rows of the CSV file
def PreferenceTransformed():
    datafile2 = open('RawData2.CSV','r')

    Data = datafile2.readlines()
    Data02 = []


    for line in Data:
        Data02.append(line.split(','))
    datafile2.close()

#Make list of lists with float values corresponding to the prefernces from CSV strings ------------------------------------------------------------
# each row contains the preference data for each respondent corresponding to each configuration

    n = len(Data02)
    nsub = len(Data02[0])

    rows = range(n)
    del rows[0]
    columns = range(nsub)
    del columns[0]

    exec('Data2 = '+'['+'[],'*n+']')

    L = []
    for line in rows:
        for charz in columns:  
            L.append(eval(Data02[line][charz]))
        Data2[line] = L
        L = []

    del Data2[0], rows, columns, Data02, L, Data

    # Transform the data into most preferred having highest value--------------------------------------------

    n = n - 1
    nsub = nsub - 1

    for line in range(n):
        for charz in range(nsub):
            Data2[line][charz] = float((nsub+1) - Data2[line][charz])
    return Data2


#######################################################################################
# This function will convert Data1 (dummy product configuration data)
# into B; a matrix to be used in the regression with ones for first column
# Input -> Data1 ; set of product configurations under study in dummy variable form
# Output -> B 
#######################################################################################

def X(Data1):
    n = len(Data1)
    m = len(Data1[0])
    exec('B = '+'['+'[1.],'*n+']')

    for i in range(n):
        for j in range(m):
            B[i].append(float(Data1[i][j]))
            
    return B

##############################################################################
# This function converts all entries in a matrix into deviations from the
# mean of the column values
# Input -> A; any matrix
# Output -> A; Matrix with all entries deviations with respect to mean
# of columns of input A.
#########################################################################
    

def matdevs(A):
    n = len(A)
    m = len(A[0])
    exec('d = '+'['+'0.,'*m+']')

    for i in range(n):
        for j in range(m):
            d[j] = d[j]+A[i][j]
  
    for i in range(m):
        d[i] = d[i]/n



    for i in range(n):
        for j in range(m):
            A[i][j] = A[i][j]-d[j]
    return A

##############################################################################
# This function converts all entries in a vector into deviations from the
# mean
# Input -> a; any vector
# Output -> a; vector with all entries deviations with respect to mean.
#########################################################################

def vecdevs(a):
    n = len(a)
    d = 0.
    for i in range(n):
        d = d + a[i]
    d = d/n

    for i in range(n):
        a[i] = a[i]-d
    return a

####################################################################################
# This function makes the configuration binary code into dummy variable binary code

# Input -> RawData3 is a CSV, with NO EMPTY TRAILING ENTRIES. Each row represents the different configurations
#          The last row (FC) of this file should contain the number in each category at the end entry of each
#          category
# Output -> Data1: Dummy variable version of binary format feature data
#           FC: which contains the dummy variable attribute category widths
#           
# m = number of attribute configurations
# READ FILE AND ASSIGN TO Data1 list of lists which contain string elements 
# Each list inside Data1 corresponds to the rows of the CSV file
###########################################################################
def DummyConvertSelection():

    datafile1 = open('RawData3.CSV','r')

    Data = datafile1.readlines()
    Data01 = []
    datafile1.close()

    for line in Data:
        Data01.append(line.split(','))

    del Data
# Make array with (0,1) corresponding to presence or not of a feature value

    m = len(Data01)-2
    mval = len(Data01[0])

    Attributes = Data01[0] # Contains the names of the attributes
    FC = Data01[-1]        # Contains the attribute category length information
    del FC[0]
    del Data01[0], Data01[-1]


    rows = range(m)
    columns = range(mval)
    del columns[0]


    exec('Data1 = '+'['+'[],'*m+']')

# Loop creates ordered attribute value data
    L = []
    for line in rows:
        for charz in columns:
            L.append(eval(Data01[line][charz]))
        Data1[line] = L
        L = []

# Make a list with the widths of the attribute categories
    FC1 = []
    for e in range(len(FC)):
        if FC[e] != '':
            FC1.append(eval(FC[e]))
    FC = FC1
    del FC1


# Erase first attribute of each category; -----{could have made another Data01 that takes only dummy vars from Data1}-------------------------------------------------------------------------------------------------

    lenFC = len(FC)

    for i in range(m):
        c = 0
        c1 = 0
        for j in range(len(FC)):
            del Data1[i][c-c1]
            c1 = c1 + 1
            c = c + FC[j]



    return [Data1]


##############################################################################
# Market Simulation with the selection of product configurations in RawData3
##############################################################################


def MarketSimulation(coefs, Prods, leny):



    Utility = []
    lenProds = len(Prods)
    for i in range(lenProds): # Calculate utility from coeficients of regression
        a = LinearAlgebra.matvec(coefs,Prods[i])
        Utility.append(a)



    Utility = LinearAlgebra.transpose(Utility)

    for i in range(len(Utility)):
        a = 0
        for j in range(len(Utility[0])):
            Utility[i][j] = 1.4**Utility[i][j]     ## The 1.35 is raised to the power of the Utilities. There is nothing special about 1.35 or e {natural exponent used in the Excel sheet} - its just to conform share numbers to the excel sheet.
            a = a + Utility[i][j]                   ## The lower the number is the less affected by extreme numbers the model is. It has to be above 1 to make sense; if not, least utility would mean most preffered.

        
        for j in range(len(Utility[0])):
            Utility[i][j] = Utility[i][j]/a

    Utility = LinearAlgebra.transpose(Utility)

            
    Logit = []
    for i in range(len(Utility)): # Prepare list of results for logit choice rule
        a = sum(Utility[i])/len(Utility[i])
        Logit.append(a)

    return Logit






