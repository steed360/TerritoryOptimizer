
'''

TerritoryOptimizer.py

Match a number of shops to a number of offices with the 
aim of reducing the overall distance between shops and 
offices.

---------------------------------------------------------

*** Usage 1 (real world usage) :

$ python TerritoryOptimizer.py <input file path> <output file path>
$ more <output file path>

(see further below for details of input & output files) :
 
After running the program you can paste both input and output csv files 
into a spreadsheet. By summing the products of the two matrices the 
cost of the program's solution can be verified.

*** Usage 2 (test mode) :

$ python MainModule.py test
$ more output.csv

(this executes the function test() and in that function you 
can change the number of shops and offices)

---------------------------------------------------------------

Before running this, you need to install "pulp" (see pre-requisites 
below). 

---------------------------------------------------------------

Full Description:

The program receives a distance (cost) matrix representing distance of each shop (rows) 
from each office (columns). The aim is match every shop to one office in the 
least expensive way overall.   

The solution will respect 3 constraints:

- C1 : Each shop is allocated to one office only
- C2 : At least C2 shops must be allocated to each office
- C3 : No more than C2 shops are allocated to a single office 

C2 and C3 can be set by modifying the global variables below.

(it would be easy to add in other constraints - e.g. a maximum
on any shop-office distance). It may be possible to set an 
objective which minimizes average, rather than total distance.

The program outputs a 'solution matrix' which has the same 
dimensions as the cost matrix but consists only of ones and 
zeros.  A '1' indicates that a shop (row) is matched to 
an office (column).

---------------------------------------------------------------

File Format

The input file should be a CSV in matrix arrangement.  
An example input file is:

BOF (beginning of file)
<space>,office 1, office 2
shop 1,5,150
shop 2,20, 135
shop 3,90, 50
shop 4,60, 35
shop 5,360, 500
EOF

The output file has the same format.

If you run the program in test mode, it will generate 
example input and output files for you.

---------------------------------------------------------------

Pre-requisites
- python 2.5+, numpy
- Install pulp
  $ sudo easy_install -U pulp
  $ sudo apt-get install glpk 

( I am not strictly sure that the glpk package is necessary, so it 
might be worth a try without this)

See:
http://www.coin-or.org/PuLP/main/installing_pulp_at_home.html
http://packages.python.org/PuLP/CaseStudies/
http://stackoverflow.com/questions/7728313/python-pulp-using-with-matrices


'''

import numpy
from pulp import *

C2_MIN_SHOPS_PER_OFFICE = 0
C3_MAX_SHOPS_PER_OFFICE = 1

TEST_NUM_COLS = 11
TEST_NUM_ROWS = 330


def WriteOutputFile (fileName, matrix, officeList, shopList):

    '''
    '''

    numOffices = len (officeList)    
    numShops   = len (shopList )

    numShops         = len ( matrix [:,0] )
    numOffices       = len ( matrix [0,:] )

    f = open ( fileName, 'w' )
    header = ',' + str (officeList).replace ("[", "").replace ("]", "").replace("'",'')
    f.write (header + '\n')

    for i in  range ( numShops)   :

        data = shopList [i] + ','

        data += str (matrix[i]).replace("[ ", "").replace ("[", "").replace ("]", "").replace ('  ', ',').replace (' ', ',')
      
        f.write (data  + "\n")

    f.close ()    

def ReadInputFile (inputFilePath):

    '''

    Read an input file of the correct type.

    Returns 3 variables
    - List of offices
    - List of shops
    - Matrix of cost data.
 
    TODO Good exceptions to anticipate would be
    -  file not found, can't open file
    Good exception to create would be
    - file out of format exception

    '''

    inFileRef = open ( inputFilePath )
    lineOneData = inFileRef.readline ()

    # Collect all columns but the last one
    officeList = lineOneData.split (',')[1:]
    shopsList  = []

    dataRows = inFileRef.readlines ()
    numRows  = len (dataRows)  
    numCols  = len (officeList)

    matrix = numpy.zeros (numRows * numCols ).reshape ( numRows, numCols )

    for rowNumber in range ( numRows ) :

        inLineData = dataRows[rowNumber].replace ('\n','').split (',')

        data = [float(y)   for y in inLineData[1:]  ]
        shopsList.append ( inLineData [0] )
        matrix [ rowNumber , : ] = data

    inFileRef.close ()
    return officeList, shopsList, matrix

def PulpSolve (inMatrix):

    ''' 
    Returns a 1/0 matrix SolutionMatrix where
    sum,ij (SolutionMatrix [ij] * costMatrix [ij] is minimized

    Subject to constraints
    - C1: 1 shop per row
    - 15-20 shops per column
    - Every cell in SolutionMatrix has value 1 or 0
    ''' 

    prob = LpProblem("Shop Assignment",LpMinimize)

    print "set up problem"

    # Loop through every cell, giving them a name.
    # As you go through add them to 3 dictionaries.
    # - dictAllCells 
    # - lstDictRowCells ( a list of dictionaries )
    # - lstDictColCells ( a list of dictionaries )

    numRows         = len ( inMatrix [:,0] )
    numCols         = len ( inMatrix [0,:] )

    colsSeq         = range (numCols)
    rowsSeq         = range (numRows)

    # Create the decision variables (equivalent to 'adjustable cells
    # in Excel Solver. Values are 1 or 0.  This dicts function is a 
    # black box but it seems to expand out the two lists
    # so that you get [0][0], [0][1], [0][n], etc, [1][0] etc.

    decVars = LpVariable.dicts("vars2",(rowsSeq,colsSeq),0,1,LpInteger)

    print "set up decision variables"

    # Set up the objective function (to be minimize)
    prob += pulp.lpSum([decVars[i][j]*inMatrix[i,j] for i in rowsSeq for j in colsSeq] ),\
            "Set up objective function"

#    print prob

    # Constraint C1 (row total) - a shop can only be assigned to one office
    for i in rowsSeq:
        prob += lpSum([decVars[i][j] for j in colsSeq] ) == 1, ""
   
    # Constraint C2 (column total) - min shops per office/column
    for j in colsSeq:
        prob += lpSum([decVars[i][j] for i in rowsSeq] ) >= C2_MIN_SHOPS_PER_OFFICE, ""    

    # Constraint C3 (column total) - min shops per office/column
    for j in colsSeq:
        prob += lpSum([decVars[i][j] for i in rowsSeq] ) <= C3_MAX_SHOPS_PER_OFFICE, ""    

    # but this works well enough for the moment.
    prob.solve()
    print "ran solver"

    # For the moment present the solution as a matrix of 1s and 0s.

    solMatrix = inMatrix.copy ()
    solMatrix [:,:] = 0

    print "created solution matrix"

    for i in rowsSeq:
        for j in colsSeq:
            if value ( decVars[i][j]  ) == 1:
                solMatrix [i,j] = 1

    print "updated solution matrix"

    totalCost = (solMatrix * inMatrix).sum ()
    avCost    = float ( totalCost ) / float (numRows)

    print "Total Distance in this solution is : " + str( int (totalCost) )
    print "Average distance  in this solution is : " + str( int(avCost) )


    return solMatrix          

def Main (inputPath, outputPath):

    print "--------------------------"
    print "... reading input file "
    print "--------------------------"

    offices, shops, mat = ReadInputFile (inputPath)

    print "--------------------------"
    print "... solving problem "
    print "--------------------------"

    res = PulpSolve ( mat )

    print "--------------------------"
    print "... writing solution matrix "
    print "--------------------------"
        

    print res
    WriteOutputFile (outputPath, res , offices , shops )

    print "--------------------------"
    print "... Output written to " + outputPath
    print "--------------------------"


def createTestFile (inFileName, numRows, numCols):

#    cm = numpy.random.randint(200, size=(numRows, numCols))
    cm = numpy.arange ( numRows * numCols ).reshape(numRows, numCols )

    lstOffices = ['off'  + str (i)  for i in range ( numCols)]   
    lstShops   = ['shop' + str (i)  for i in range ( numRows)]   

    WriteOutputFile ( inFileName, cm, lstOffices, lstShops)

if __name__ == '__main__': 
  
    firstArg  = sys.argv [1] 

    if firstArg in ['Test', 'TEST', 'test']:

        # Specify the size of the problem here.
        numRows = TEST_NUM_ROWS
        numCols = TEST_NUM_COLS 

        createTestFile ('TestInput.csv', numRows, numCols) 

        C2_MIN_SHOPS_PER_OFFICE = (float (numRows) / float (numCols) ) - 3

        if C2_MIN_SHOPS_PER_OFFICE < 0: C2_MIN_SHOPS_PER_OFFICE = 1
        C3_MAX_SHOPS_PER_OFFICE = (float (numRows) / float (numCols) ) + 3
        if C3_MAX_SHOPS_PER_OFFICE > numRows: C3_MAX_SHOPS_PER_OFFICE = numRows

        print "*********************************************"
        print "running test optimization..."
        print "Match " + str ( numRows ) + " shops to " + str (numCols) + " shops"
        print "Allow " + str ( C2_MIN_SHOPS_PER_OFFICE ) + " to " + str (C3_MAX_SHOPS_PER_OFFICE ) + " shops per office "

        print "*********************************************"

        firstArg =  'TestInput.csv'   
        secondArg = 'TestOutput.csv'  

    else:
        if  len ( sys.argv ) < 2  :
            secondArg = sys.argv [2]
        else: 
            secondArg = "output.csv"
 
    Main ( firstArg, secondArg )


