from sklearn.ensemble import AdaBoostClassifier
from commons import variables
import numpy as np


def learn(x, y, test_x):
    # set sample weight
    weight_list = []
    for j in range(len(y)):
        if y[j] == "0":
            weight_list.append(variables.weight_0_ada)
        if y[j] == "1000":
            weight_list.append(variables.weight_1000_ada)
        if y[j] == "1500":
            weight_list.append(variables.weight_1500_ada)
        if y[j] == "2000":
            weight_list.append(variables.weight_2000_ada)

    clf = AdaBoostClassifier(n_estimators=variables.n_estimators_ada, learning_rate=variables.learning_rate_ada).fit(x,
                                                                                                                     y,
                                                                                                                     np.asarray(
                                                                                                                         weight_list))
    prediction_list = clf.predict(test_x)
    prediction_list_prob = clf.predict_proba(test_x)

    return prediction_list, prediction_list_prob
