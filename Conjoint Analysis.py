# This script incorporates the part worth and attribute importance
# corresponding to the "PW and AI" worksheet of the Excel file.
#
# Input -> Data1, Data2, FC
# Output -> Attribute Importance Chart and Part worth graphing data

#########################################################################
# Load modules
#########################################################################
import LinearAlgebra, Cook, math, copy

########################################################################
# Load Data
########################################################################
D = Cook.DummyConvert()
Prods = Cook.DummyConvertSelection()
Prods = Prods[0]
Data1 = D[0]
FC = D[1]
Attr = D[2]
Attrz = copy.deepcopy(Attr)
del Attr[0]
del D

Data1 = Cook.matdevs(Data1)

X = Cook.X(Data1)
Xdash = LinearAlgebra.transpose(X)
B = LinearAlgebra.matmat(Xdash,X)
Data2 = Cook.PreferenceTransformed()



#########################################################################
# Regression Analysis on each respondents data
# Input -> Data1, Data2
# Output -> coefs; contains the coeficients of regression
#########################################################################


Y = []
for i in range(len(Data2)):
    Y.append(Cook.vecdevs(Data2[i]))
leny = len(Y)

Y = LinearAlgebra.transpose(Y)
Y = LinearAlgebra.matmat(Xdash,Y)
Y = LinearAlgebra.transpose(Y)



coefs = []
for i in range(leny):
    A = copy.deepcopy(B)
    coefs.append(LinearAlgebra.solver(A,Y[i]))



#########################################################################
# Averages of coeficients of regression
#########################################################################
leny0 = len(Y[0])

exec('d = '+'['+'0.,'*leny0+']')

for i in range(leny):
    for j in range(len(Y[0])):
        d[j] = d[j]+coefs[i][j]

        
for i in range(leny0):
    d[i] = d[i]/leny
del d[0]


#########################################################################
# Attribute Importance Chart
#########################################################################
lenFC = len(FC)
FC0 = [0]


c = 0
for i in range(lenFC): # Make FC0 a cumulative version of FC to use it to manipulate list data
    c = c + FC[i]
    FC0.append(c)



acc = []
for i in range(lenFC): # Group coeficients of regression according to attribute category
    a = d[FC0[i]:(FC0[i+1])]
    acc.append(a)

exec('d = '+'['+'[0.],'*lenFC+']') # d is a list that contains lenFC lists inside


for i in range(lenFC):    # Make the coeficients into their absolute values
    for j in range(len(acc[i])):
        d[i].append(abs(acc[i][j]))
        
maxi = [];
for i in range(lenFC):  # Find maximum value of each category and place it in maxi
    maxi.append(max(d[i]))

AttributeImportance = []
summaxi = sum(maxi)

for i in range(lenFC):  # Make the chart of attribute importance
    AttributeImportance.append(['Category:' + str(i+1),maxi[i],str(100*maxi[i]/summaxi)+ ' %'])
AttributeImportance.append(['Total:' ,summaxi,'100'+ ' %'])



##################################################################################
# Produce graphing data for each category
################################################################################


PWGraphs = []
for i in range(lenFC):
    b = [0.]
    a = Attr[0:len(d[i])]
    b = b + acc[i]

    del Attr[0:len(d[i])]
    PWGraphs.append([a,b])


    

##############################################################################
# Market Simulation with the selection of product configurations in RawData3
##############################################################################

for i in range(leny): #Remove Intercept data from Coeficients of regression
    del coefs[i][0]

Utility = []
lenProds = len(Prods)
for i in range(lenProds): # Calculate utility from coeficients of regression
    a = LinearAlgebra.matvec(coefs,Prods[i])
    Utility.append(a)

Utility = LinearAlgebra.transpose(Utility)

for i in range(len(Utility)):
    a = 0
    for j in range(len(Utility[0])):
        Utility[i][j] = 2.71828**Utility[i][j]     ## The 1.35 is raised to the power of the Utilities. There is nothing special about 1.35 or e {natural exponent used in the Excel sheet} - its just to conform share numbers to the excel sheet.
        a = a + Utility[i][j]                   ## The lower the number is the less affected by extreme numbers the model is. It has to be above 1 to make sense; if not, least utility would mean most preffered.

    
    for j in range(len(Utility[0])):
        Utility[i][j] = Utility[i][j]/a

Utility = LinearAlgebra.transpose(Utility)
  

Logit = []
Props = []
for i in range(len(Utility)): # Prepare list of results for logit choice rule
    a = sum(Utility[i])/len(Utility[i])
    Logit.append('Product_'+ str(i+1)+ ': ' + str(a*100) + '%')
    Props.append(a)

a = max(Props)
pos = 0

###############################################################################
# Elasticity analysis on the products
###############################################################################

Prices = PWGraphs[0][0]

for i in range(len(Prices)):        # make prices into float data
    Prices[i] = float(Prices[i])


for i in range(len(Prices)-1):    # Clear price information from the product configuration coming under study
        Prods[pos][i] = 0




Logits = [Cook.MarketSimulation(coefs, Prods, leny)]

for i in range(len(Prices)-1):   # Elasticity analysis
    Prods[pos][i] = 1
    Logits.append(Cook.MarketSimulation(coefs, Prods, leny))   
    Prods[pos][i] = 0


################################################################################
# Revenue Maximization
################################################################################

maxi = []
for i in range(len(Prices)):
    maxi.append(Logits[i][pos]*Prices[i])
print 'Attribute Importance: \n',AttributeImportance,'\n \n','Part Worth Graphing Data: \n',PWGraphs,'\n \nLogit Choice Output: \n' ,Logit,'\n\nElasticity Analysis\n' ,Logits, '\n\nRevenue from Elasticity Analysis\n', maxi, '\n \nMaximum Revenue: ' , max(maxi), 'at', Prices[maxi.index(max(maxi))] ,'Dollars'         
