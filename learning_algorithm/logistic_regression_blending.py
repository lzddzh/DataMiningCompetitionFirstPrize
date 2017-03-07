from sklearn.linear_model import LogisticRegression
from commons import variables
from commons import tools
from scipy.stats import mode


def learn(x, y, test_x):
    # set sample weight


    weight_list = []
    for j in range(len(y)):
        if y[j] == "0":
            weight_list.append(variables.weight_0_lr)
        if y[j] == "1000":
            weight_list.append(variables.weight_1000_lr)
        if y[j] == "1500":
            weight_list.append(variables.weight_1500_lr)
        if y[j] == "2000":
            weight_list.append(variables.weight_2000_lr)

    clf = LogisticRegression().fit(x, y, weight_list)

    prediction_list = clf.predict(test_x)

    return prediction_list
