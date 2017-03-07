from sklearn.ensemble import GradientBoostingClassifier
from commons import variables
from commons import tools
from scipy.stats import mode


def learn(x, y, test_x):
    # set sample weight


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

    clf = GradientBoostingClassifier(loss='deviance', n_estimators=variables.n_estimators_gdbt,
                                     learning_rate=variables.learning_rate_gdbt,
                                     max_depth=variables.max_depth_gdbt, random_state=variables.random_seed,
                                     min_samples_split=variables.min_samples_split_gdbt,
                                     min_samples_leaf=variables.min_samples_leaf_gdbt,
                                     subsample=variables.subsample_gdbt,
                                     max_features=variables.max_feature_gdbt).fit(x, y, weight_list)
    prediction_list = clf.predict(test_x)
    prediction_list_prob = clf.predict_proba(test_x)
    # print prediction_list_prob
    # print clf.classes_

    return prediction_list,prediction_list_prob
