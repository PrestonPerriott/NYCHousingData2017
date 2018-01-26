import numpy as np  #Used for linear algebra
import pandas  #Used for data processing, CSV file I/O
from numpy import mean, median #While this is added in the 'import numpy as np', useful to note, we need these to print out lists
from scipy.stats import ttest_ind
#A ttest is a stat test to estimate if the diff of two measured groups is reliable
#Using an independant samples ttest b/c were comparing two groups
#An Analysis of Variance ttest does this with more than two groups
from scipy.stats import probplot #needed for qqplot
import matplotlib.pyplot as plt #Visualization Library
import pylab
import time, datetime
from subprocess import check_output
import os
import cv2

#Its worth Command clicking through all of the functions you're not familiar with
#TODO All the Exception Handling

class fileReader():
    def __init__(self, file):
        #initialize a fileReader object                 #A class so things are more easily mutatable
        if self.checkPath(file):
            self.file = file
            self.dataFrame = pandas.read_csv(self.file) #Read Data into 'dataFrame' object
            self.summary = self.dataFrame.describe()    #Summarize said dataFrame object
            self.columns = self.dataFrame.columns       #Grab all the columns from csv
            self.head = self.dataFrame.head()           #Throws first few lines of doc
        return

    def createHisto(self, numOfPlots, data, labels, loc, title, alpha):
        #If num of plots is greater than two, we should assume data is an array of arrays [ [1,2,3,4], [17, 27, 67, 23] ]
        if numOfPlots >= 2:
            x = len(data)
            i = 0
            while i < x:
                plt.hist(data[i], alpha=alpha, label=labels[i])
                i += 1
            plt.legend(loc=loc)
            plt.title(title)
        else:                                           #If we dont have more than two arrays to plot, we should expect to plot one
            plt.hist(data, alpha=alpha, label=labels, title=title)
            plt.legend(loc=loc)
        return plt

    def checkDistribution(self, dataArray, dist, plot): #Line of best fit function
        if len(dataArray) >= 2:
            probplot(dataArray, dist=dist, plot=plot)
            plot.show()
            return

    def checkPath(self, file):
        if os.path.isfile(file):
            return True
        else:
            return False

    def printColumn(self, column):                      #Add some functionality that helps user search for correct column
        colToPrint = self.dataFrame[column]             #Like auto correct name, if column has numerics & which are labels
        print colToPrint

if __name__ == '__main__':

    newReader = fileReader('nyc-rolling-sales.csv')     #specifiy the file and path if needed
    print '\n\n\n'

    # newReader.printColumn('ADDRESS')                  #Class func to just pass column name to return whole column
    # newReader.printColumn('SALE PRICE')
    salePrice = newReader.dataFrame['SALE PRICE']
    builtYear = newReader.dataFrame['YEAR BUILT']

    refactoredPrices = []                               #Loop takes salePrice column, swaps all '-' for 0's
    for i in range(0, len(salePrice), 1):
        if salePrice[i] == '-' or salePrice[i] == ' - ' or salePrice[i] == ' -  ':
            refactoredPrices.append(float(0))
        else:
            refactoredPrices.append(float(salePrice[i]))

    print '\n\n'
    print newReader.columns                             #Pands func for viewing all of the columns in csv

    plt.title("2016 New York Property Construction Dates")
    plt.hist(builtYear[0:500], bins=20, edgecolor='black')   #Creates the histogram #[0:200] dictates i want the 0th to the 200th items used

    # A histogram is a type of chart where the x-axis (along the bottom) is the range of numeric values of the variable,
    # chopped up into a series of bins. For example, if the range of a value is from 0 to 12,
    # it might be split into four bins, the first one being 1 through 3, the second being 4 through 6,
    # the third 7 through 8, and the fourth 9 through 12.
    # The y-axis (along the side) is the count of how many observations fall within each bin.
    # Essentially measures the frequency of a variable, rather than track a change over time
    plt.ylabel('Volume of Properties')
    plt.xlabel('Year Built')
    plt.show()
    # plt.hist(newReader.dataFrame['BLOCK'].astype(np.float))  #astype forces an entire grouping to change types

    hood = newReader.dataFrame['NEIGHBORHOOD']
    #print hood
    print '\n'

    theDale = []
    chelsea = []

    dalePrices = []
    chelseaPrices = []
    for locale in range(0, len(hood), 1):
        if hood[locale] == 'CHELSEA':
            chelsea.append(hood[locale])
            chelseaPrices.append(refactoredPrices[locale])
        elif hood[locale] == 'RIVERDALE':
            theDale.append(hood[locale])
            dalePrices.append(refactoredPrices[locale])

    print 'Number of Chelsea properties : '
    print len(chelsea)
    print '\n'
    print 'Number of Riverdale properties : '
    print len(theDale)

    print '\n\n\n'
    chelseaStats = zip(chelsea, chelseaPrices)
    daleStats = zip(theDale, dalePrices)

    print 'The mean Chelsea prices are : '
    #print newReader.dataFrame['SALE PRICE'][newReader.dataFrame['NEIGHBORHOOD'] == 'RIVERDALE'].mean() #Only works for a dataFrame object
    print np.mean(chelseaPrices)
    print '\n'

    print 'The median Chelsea prices are : '
    print np.median(chelseaPrices)

    #Prior to ttest we should make sure the variable is normally distributed,
    #Plotting a QQPlot to check normality, hoping that most points are along the center diagonal
    #basic line of best fit
    newReader.checkDistribution(chelseaPrices,"norm",pylab)
    # probplot(chelseaPrices, dist="norm", plot=pylab)
    # pylab.show()


    print '\n'
    comparison = ttest_ind(chelseaPrices, dalePrices, equal_var=False)
    print 'The TTest compared object returns a statistic value of :'
    print comparison[0]
    print '\n'

    print 'The TTest compared object returns a p-value of :'
    print comparison[1]
    print '\n'

    dataArray = [chelseaPrices[0:100], dalePrices[0:100]]
    graph = newReader.createHisto(2, dataArray, ['chel','dale'],'upper right', 'BX vs Chelsea Prices', 0.5)
    graph.show()


















