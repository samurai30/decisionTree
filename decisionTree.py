import pandas as pd
import numpy as np
from collections import Counter


class DecisionTree:
    def __init__(self, value, terminate):
        self.child = None
        self.terminate = terminate
        self.value = value


def decision_init(path):
    dt = pd.read_excel(path)
    column_length = len(dt.columns)-1
    column_list = list(dt.columns)
    switch = {}
    print('Column names for the given Document:')
    for i in range(len(column_list)):
        switch[i] = column_list[i]
    print(switch)

    decision_input = int(input('Please Select the Decision Column Name (Enter corresponding number):'))

    if decision_input < column_length:
        temp_value = column_list[decision_input]
        column_list[decision_input] = column_list[column_length]
        column_list[column_length] = temp_value

    return {'decision_table': dt[column_list], 'classification_column': column_list[decision_input]}


def get_column_entropy(dt, class_name, length):
    column = list(dt.columns)
    unq = np.unique(dt[column[0]])
    column_entropy = {}
    count_column = Counter(dt[column[0]])
    for i in unq:
        temp = dt.loc[dt[column[0]] == i]
        column_entropy[i] = entropy_classification(temp[class_name], len(temp))['Sample_Space']
    total_entropy = 0
    for i in column_entropy:
        total_entropy = total_entropy + (count_column[i]/length * column_entropy[i])

    return total_entropy


def entropy_classification(class_table, length):
    sample_space = dict(Counter(class_table))
    keys = list(sample_space.keys())

    entropy = 0
    if len(keys) > 1:
        pos_num = keys[0]
        neg_num = keys[1]

        if sample_space[pos_num] == sample_space[neg_num]:
            entropy = 1
        else:
            positive = sample_space[pos_num] / length
            negative = sample_space[neg_num] / length
            entropy = - positive * np.log2(positive) - negative * np.log2(negative)

    return {'Sample_Space': entropy}


def get_gain(dt, class_name):
    sample_length = len(dt)
    sample_entropy = entropy_classification(dt[class_name], sample_length)

    classification_table = list(dt)
    classification_table.remove(class_name)
    gain = {}
    for column in classification_table:
        gain[column] = sample_entropy['Sample_Space'] - get_column_entropy(dt[[column, class_name]], class_name, sample_length)

    return gain


init_dt = decision_init('TestSheet.xlsx')
# print(init_dt['decision_table'])
get_gain(init_dt['decision_table'], init_dt['classification_column'])

root = DecisionTree('Tree', False)

root.child = [DecisionTree('tree1', False), DecisionTree('Tree2', True)]

root.child[0].child = [DecisionTree('tree3', True)]


def trav(roots):
    print('Hello'+roots.value)

    if roots.terminate is False:
        for i in roots.child:
            trav(i)


trav(root)

