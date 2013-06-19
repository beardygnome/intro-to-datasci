from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import numpy
import sys

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation as cv

# set constants for string variable to float conversion
MALE = 0.0
FEMALE = 1.0

SOUTHAMPTON = 0.0
CHERBOURG = 1.0
QUEENSTOWN = 2.0

def import_data(csv_filepath):
    csv_file = csv.reader(open(csv_filepath, "rb"))
    header = csv_file.next()
    data = []

    for row in csv_file:
        data.append(row)

    return numpy.array(data)

def gender_to_float(data, gender_index):
    """convert gender column to float constants"""
    males = data[:, gender_index] == "male"
    females = data[:, gender_index] == "female"

    data[males, gender_index] = MALE
    data[females, gender_index] = FEMALE

def port_to_float(data, port_index):
    """convert embarkation port to float constants"""
    data[data[:, port_index] == "C", port_index] = CHERBOURG
    data[data[:, port_index] == "Q", port_index] = QUEENSTOWN
    data[data[:, port_index] == "S", port_index] = SOUTHAMPTON

    # fill gaps in port
    non_blank_ports = data[:, port_index] != ""
    blank_ports = data[:, port_index] == ""

    most_common_port = int(numpy.mean(
            data[non_blank_ports, port_index].astype(float)))
    data[blank_ports, port_index] = most_common_port

def infill_age(data, gender_index, age_index, class_index):
    """fill gaps in age"""
    classes = set()

    for i in xrange(numpy.size(data[:, class_index])):
        passenger_class = data[i, class_index]
        classes.add(passenger_class)

    males = data[:, gender_index].astype(float) == MALE
    females = data[:, gender_index].astype(float) == FEMALE
    non_blank_ages = data[:, age_index] != ""
    blank_ages = data[:, age_index] == ""

    for class_ in classes:
        this_class = data[:, class_index] == class_
        male_ages = data[males & non_blank_ages & this_class, age_index].astype(float)
        median_male_age = numpy.median(male_ages)

        female_ages = data[females & non_blank_ages & this_class, age_index].astype(float)
        median_female_age = numpy.median(female_ages)

        # set blank male ages to the median age of males
        data[males & blank_ages & this_class, age_index] = median_male_age

        #set blank female ages to the median age of females
        data[females & blank_ages & this_class, age_index] = median_female_age

def infill_fare(data, class_index, fare_index):
    """fill in the gaps in fare price"""
    classes = set()

    for i in xrange(numpy.size(data[:, class_index])):
        passenger_class = data[i, class_index]
        classes.add(passenger_class)

    for class_ in classes:
        this_class = data[:, class_index] == class_
        non_blank_fares = data[:, fare_index] != ""
        blank_fares = data[:, fare_index] == ""

        fares = data[this_class & non_blank_fares, fare_index].astype(float)
        median_fare = numpy.median(fares)

        data[this_class & blank_fares, fare_index] = median_fare

def prepare_training_data(data):
    """prepare the training dataset"""
    gender_to_float(data, 3)
    port_to_float(data, 10)
    infill_age(data, 3, 4, 1)
    infill_fare(data, 1, 8)

    # remove string columns
    data = numpy.delete(data, [2, 7, 9], 1)

    # split data into training and testing subsets
    training, testing = cv.train_test_split(data, test_size=0.25)

    return training, testing

def predict_for_test_data(model, filepath, output_path):
    """apply the model to the test data"""
    print("Predicting for the test data")

    data = import_data(filepath)

    gender_to_float(data, 2)
    port_to_float(data, 9)
    infill_age(data, 2, 3, 0)
    infill_fare(data, 0, 7)

    data = numpy.delete(data, [1, 6, 8], 1)

    try:
        output = model.predict(data)
    except Exception as ex:
        print(str(ex))
    else:
        csv_in = csv.reader(open(filepath, "rb"))
        csv_out = csv.writer(open(output_path, "wb"))

        header = csv_in.next()
        header.insert(0, "prediction")
        #csv_out.writerow(header) # advised not to submit the header to Kaggle

        i = 0

        for row in csv_in:
            row.insert(0, output[i].astype(int))
            csv_out.writerow(row)

            i += 1

def create_model(data, model_type):
    """create the random forest"""
    print("Creating forest...")

    models = {"extra trees" : ExtraTreesClassifier,
                "gradient boosting" : GradientBoostingClassifier,
                "random forest" : RandomForestClassifier}

    target_variable = data[:, 0]
    data = data[:, 1:]
    model = None

    if model_type in models:
        model = models[model_type](n_estimators=100)

    if model is not None:
        model.fit(data, target_variable)
    else:
        print("No model created, exiting...")
        sys.exit(1)

    return model

def score_model(data, model):
    target_variable = data[:, 0]
    data = data[:, 1:]

    print('Model accuracy: {0}'.format(model.score(data, target_variable)))

if __name__ == "__main__":
    #training
    data = import_data("../csv/train.csv")

    males = data[:, 3] == "male"
    age = data[:, 4] != ""


    training, testing = prepare_training_data(data)
    #model = create_model(training, "random forest")
    #model = create_model(training, "gradient boosting")
    model = create_model(training, "extra trees")
    score_model(testing, model)

    #predicting
    file_in = "../csv/test.csv"
    file_out = "../csv/my_et_output.csv"

    predict_for_test_data(model, file_in, file_out)
