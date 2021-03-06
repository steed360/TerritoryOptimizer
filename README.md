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

