# The first thing to do is to import the relevant packages that I will need for
# my script, these include the Numpy (for maths and arrays) and csv for reading
# and writing csv files.
# If I want to use something from this I need to call csv.[function] or
# np.[function].

from __future__ import absolute_import, division, print_function, unicode_literals

import csv as csv
import numpy as np

# open up the csv file in to a Python object
csv_file_object = csv.reader(open('../csv/train.csv', 'rb'))

#The next() command just skips the first line which is a header
header = csv_file_object.next()

data=[]

# run through each row in the csv file adding each row to the data variable
for row in csv_file_object:
    data.append(row)

# then convert from a list to an array
# be aware that each item is currently a string in this format
data = np.array(data)

# the size function counts how many elements are in the array and sum (as you
# would expects) sums up the elements in the array.

# Model 1, gender
number_passengers = np.size(data[:, 0].astype(float))
number_survived = np.sum(data[:, 0].astype(float))
proportion_survivors = number_survived / number_passengers

women_only_stats = data[:, 3] == "female"       # this finds where all
                                                # the elements in the gender
                                                # column that equals "female"
men_only_stats = data[:, 3] != "female"		# this finds where all the
                                                # elements do not equal
                                                # female (I.e. male)

#Using the index from above we select the females and males separately
women_onboard = data[women_only_stats, 0].astype(float)
men_onboard = data[men_only_stats, 0].astype(float)

# Then we finds the proportions of them that survived
proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

#and then print it out
print('Proportion of women who survived is {0}'.format(proportion_women_survived))
print('Proportion of men who survived is {0}'.format(proportion_men_survived))

# test the model on the test data
test_file_obect = csv.reader(open('../csv/test.csv', 'rb'))
header = test_file_obect.next()
open_file_object = csv.writer(open("../csv/genderbasedmodelpy.csv", "wb"))

for row in test_file_obect:
    if row[2] == 'female':
        # insert the prediction of survived (1) at position 0
        row.insert(0, '1')
    else:
        #insert the prediction of did not survive (0)
        row.insert(0, '0')

    # write row to the new file
    open_file_object.writerow(row)

################################################################################

# Model 2, gender, passenger class and ticket price
# need to have equal ticket price bands, so set all prices of $40+ to $39
fare_ceiling = 40
data[(data[:, 8].astype(float) >= fare_ceiling), 8] = fare_ceiling - 1.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling // fare_bracket_size
number_of_classes = 3 #There were 1st, 2nd and 3rd classes on board

# define the survival table
survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

for i in xrange(number_of_classes):             #search through each class
    for j in xrange(number_of_price_brackets):  #search through each price
        women_only_stats = data[
                        # find females
                        (data[:, 3] == "female") &
                        # who were in passenger class i, i is zero-based
                        (data[:, 1].astype(float) == i + 1) &
                        # whose ticket price was greater than bin j's lower bound
                        (data[:, 8].astype(float) >= j * fare_bracket_size) &
                        # and less than bin j+1's lower bound
                        (data[:, 8].astype(float) < (j + 1) * fare_bracket_size)
                        # get column 0 (survival rate)
                        , 0]



        men_only_stats = data[
                        # find males
                        (data[:, 3] != "female") &
                        # who were in passenger class i, i is zero-based
                        (data[:, 1].astype(float) == i + 1) &
                        # whose ticket price was greater than bin j's lower bound
                        (data[:, 8].astype(float) >= j * fare_bracket_size) &
                        # and less than bin j+1's lower bound
                        (data[:, 8].astype(float) < (j + 1) * fare_bracket_size)
                        # get column 0 (survial rate)
                        , 0]

        # add to survival table
        survival_table[0,i,j] = np.mean(women_only_stats.astype(float)) #Women stats
        survival_table[1,i,j] = np.mean(men_only_stats.astype(float)) #Men stats

# Python returns NaN for any mean where there are no passengers, so set these to 0
survival_table[ survival_table != survival_table ] = 0

# assume that a survival rate of < 0.5 means no-one in that group survived and
# >= 0.5 means everyone in that group survived
survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1

# test the model on the test data
test_file_obect = csv.reader(open('../csv/test.csv', 'rb'))
fname = "../csv/genderclasspricebasedmodelpy.csv"
open_file_object = csv.writer(open(fname, "wb"))
header = test_file_obect.next()

# we are going to loop through each passenger in the test set
for row in test_file_obect:
    # for each passenger we loop through each price bin
    for j in xrange(number_of_price_brackets):
        # some passengers have no price data so try to make a float
        try:
            row[7] = float(row[7])
        # if fails: no data, so bin the fare according class
        except:
            bin_fare = 3 - float(row[0])
            break

        # if there is data see if it is greater than fare ceiling we set earlier
        if row[7] > fare_ceiling:
            # if so set to highest bin
            bin_fare = number_of_price_brackets-1
            break

        # if passed these tests then loop through each bin then assign index
        if row[7] >= j*fare_bracket_size and row[7] < (j + 1) * fare_bracket_size:
            bin_fare = j
            break

    # if the passenger is female
    if row[2] == 'female':
        # at element 0, insert the prediction from survival table
        row.insert(0,
                int(survival_table[0,float(row[0]) - 1,# passenger class
                bin_fare]))                             # ticket group
    else:
        row.insert(0,
             int(survival_table[1,float(row[0]) - 1,
             bin_fare]))

    # write out row
    open_file_object.writerow(row)
