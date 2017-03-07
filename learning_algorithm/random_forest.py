from sklearn.ensemble import RandomForestClassifier
from commons import variables
from commons import tools
from scipy.stats import mode


def learn(x, y, test_x):
    cw = {"0": variables.weight_0_rf, "1000": variables.weight_1000_rf, "1500": variables.weight_1500_rf,
          "2000": variables.weight_2000_rf}
    clf = RandomForestClassifier(n_jobs=-1,
                                 n_estimators=variables.n_estimators_rf,
                                 max_depth=variables.max_depth_rf, random_state=0,
                                 min_samples_split=variables.min_samples_split_rf,
                                 min_samples_leaf=variables.min_samples_leaf_rf,
                                 max_features=variables.max_feature_rf,
                                 max_leaf_nodes=variables.max_leaf_nodes_rf,
                                 criterion=variables.criterion_rf,
                                 min_impurity_split=variables.min_impurity_split_rf,
                                 class_weight=variables.cw_rf).fit(x, y)

    prediction_list = clf.predict(test_x)
    prediction_list_prob = clf.predict_proba(test_x)

    return prediction_list, prediction_list_prob
