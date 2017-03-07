from sklearn.ensemble import GradientBoostingClassifier
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

    clf = GradientBoostingClassifier(loss='deviance', n_estimators=variables.n_estimators_gdbt_b,
                                     learning_rate=variables.learning_rate_gdbt_b,
                                     max_depth=variables.max_depth_gdbt_b, random_state=0,
                                     min_samples_split=variables.min_samples_split_gdbt_b,
                                     min_samples_leaf=variables.min_samples_leaf_gdbt_b,
                                     subsample=variables.subsample_gdbt_b,
                                     ).fit(x, y, weight_list)
    prediction_list = clf.predict(test_x)

    return prediction_list
