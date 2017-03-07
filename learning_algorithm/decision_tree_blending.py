from sklearn import tree
from commons import variables
from commons import tools
from scipy.stats import mode


def learn(x, y, test_x):
    # set sample weight


    weight_list = []
    for j in range(len(y)):
        if y[j] == "0":
            weight_list.append(variables.weight_0_gdbt_b)
        if y[j] == "1000":
            weight_list.append(variables.weight_1000_gdbt_b)
        if y[j] == "1500":
            weight_list.append(variables.weight_1500_gdbt_b)
        if y[j] == "2000":
            weight_list.append(variables.weight_2000_gdbt_b)

    clf = tree.DecisionTreeClassifier(min_samples_split=500).fit(x, y, weight_list)
    print clf.feature_importances_

    prediction_list = clf.predict(test_x)

    return prediction_list
