""" Now the user can read in a file I want to find what make a model which uses the price, class and gender
Author : AstroDave
Date : 18th September, 2012

"""

from __future__ import absolute_import, division, print_function, unicode_literals

import csv as csv
import numpy as np

csv_file_object = csv.reader(open('../csv/train.csv', 'rb')) #Load in the csv file
header = csv_file_object.next() #Skip the fist line as it is a header
data=[] #Creat a variable called 'data'
for row in csv_file_object: #Skip through each row in the csv file
    data.append(row) #adding each row to the data variable
data = np.array(data) #Then convert from a list to an array

#in order to analyse the price collumn I need to bin up that data
#here are my binning parameters the problem we face is some of the fares are very large
#So we can either have a lot of bins with nothing in them or we can just absorb some
#information and just say anythng over 30 is just in the last bin so we add a ceiling
fare_ceiling = 40

data[data[0::,8].astype(np.float) >= fare_ceiling, 8] = fare_ceiling-1.0
fare_bracket_size = 10
number_of_price_brackets = fare_ceiling // fare_bracket_size
number_of_classes = 3 #There were 1st, 2nd and 3rd classes on board
#This reference table will show we the proportion of survivors as a function of
# Gender, class and ticket fare.
survival_table = np.zeros([2,number_of_classes,number_of_price_brackets],float)

# I can now find the stats of all the women and men on board
for i in xrange(number_of_classes):
    for j in xrange(number_of_price_brackets):

        women_only_stats = data[ (data[0::,3] == "female") \
                                 & (data[0::,1].astype(np.float) == i+1) \
                                 & (data[0:,8].astype(np.float) >= j*fare_bracket_size) \
                                 & (data[0:,8].astype(np.float) < (j+1)*fare_bracket_size), 0]

        men_only_stats = data[ (data[0::,3] != "female") \
                                 & (data[0::,1].astype(np.float) == i+1) \
                                 & (data[0:,8].astype(np.float) >= j*fare_bracket_size) \
                                 & (data[0:,8].astype(np.float) < (j+1)*fare_bracket_size), 0]

                                 #if i == 0 and j == 3:

        survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float)) #Women stats
        survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float)) #Men stats

#Since in python if it tries to find the mean of an array with nothing in it
#such that the denominator is 0, then it returns nan, we can convert these to 0
#by just saying where does the array not equal the array, and set these to 0.
survival_table[ survival_table != survival_table ] = 0.

#Now I have my proportion of survivors, simply round them such that if <0.5
#they dont surivive and >1 they do
survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1


#Now I have my indicator I can read in the test file and write out
#if a women then survived(1) if a man then did not survived (0)
#1st Read in test
test_file_obect = csv.reader(open('../csv/test.csv', 'rb'))
open_file_object = csv.writer(open("../csv/genderclasspricebasedmodelpy.csv", "wb"))

header = test_file_obect.next()

#First thing to do is bin up the price file
for row in test_file_obect:

    for j in xrange(number_of_price_brackets):
        #If there is no fare then place the price of the ticket
        #according to class
        try:
            row[7] = float(row[7]) #No fare recorded will come up as a string so
                                    #try to make it a float
        except: #If fails then just bin the fare according to the class
            bin_fare = 3-float(row[0])
            break #Break from the loop and move to the next row
        if row[7] > fare_ceiling: #Otherwise now test to see if it is higher
                                  #than the fare ceiling we set earlier
            bin_fare = number_of_price_brackets-1
            break #And then break to the next row

        if row[7] >= j*fare_bracket_size\
            and row[7] < (j+1)*fare_bracket_size:#If passed these tests then loop through
                                          #each bin until you find the right one
                                          #append it to the binned_price
                                          #and move to the next loop
            bin_fare = j
            break
        #Now I have the bin fare, the class and whether female or male we can
        #just cross ref their details with our 'survivial table
    if row[2] == 'female':
        row.insert(0,int(survival_table[0,float(row[0])-1,bin_fare])) #Insert the prediciton
                                                        #at the start of the row
        open_file_object.writerow(row) #Write the row to the file
    else:
        row.insert(0,int(survival_table[1,float(row[0])-1,bin_fare])) #Insert the prediciton
                                                        #at the start of the row
        open_file_object.writerow(row)
