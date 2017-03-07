from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from commons import variables
from commons import tools
from scipy.stats import mode


def learn(x, y, test_x):
    weight_list = []
    for j in range(len(y)):
        if y[j] == "0":
            weight_list.append(variables.weight_0_gdbt)
        if y[j] == "1000":
            weight_list.append(variables.weight_1000_gdbt)
        if y[j] == "1500":
            weight_list.append(variables.weight_1500_gdbt)
        if y[j] == "2000":
            weight_list.append(variables.weight_2000_gdbt)

    clf = KNeighborsClassifier(1, weight_list).fit(x, y)

    prediction_list = clf.predict(test_x)
    return prediction_list
