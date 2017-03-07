from sklearn import svm
from commons import variables
import numpy as np

X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y)


def learn(x, y, test_x):
    # set sample weight
    weight_list = []
    for j in range(len(y)):
        if y[j] == "0":
            weight_list.append(variables.weight_0_svm)
        if y[j] == "1000":
            weight_list.append(variables.weight_1000_svm)
        if y[j] == "1500":
            weight_list.append(variables.weight_1500_svm)
        if y[j] == "2000":
            weight_list.append(variables.weight_2000_svm)

    clf = svm.SVC(C=variables.C_svm, cache_size=10000, class_weight=None, coef0=0.0,
                  decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
                  max_iter=-1, probability=False, random_state=None, shrinking=True,
                  tol=0.001, verbose=False).fit(x, y, np.asarray(weight_list))

    prediction_list = clf.predict(test_x)
    prediction_list_prob = clf.predict_proba(test_x)

    return prediction_list, prediction_list_prob
