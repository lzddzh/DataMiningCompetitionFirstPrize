from sklearn.ensemble import ExtraTreesClassifier
from commons import variables
from commons import tools
from scipy.stats import mode


def learn(x, y, test_x):
    cw = {"0":variables.weight_0_rf, "1000":variables.weight_1000_rf, "1500":variables.weight_1500_rf, "2000":variables.weight_2000_rf}
    clf = ExtraTreesClassifier(n_jobs = -1,
                                     n_estimators=variables.n_estimators_et,
                                     max_depth=variables.max_depth_et, random_state=0,
                                     min_samples_split=variables.min_samples_split_et,
                                     min_samples_leaf=variables.min_samples_leaf_et,
                                     max_features=variables.max_feature_et,
                                     max_leaf_nodes=variables.max_leaf_nodes_et,
                                     criterion=variables.criterion_et,
                                     min_impurity_split=variables.min_impurity_split_et,
                                     class_weight=variables.cw_et).fit(x, y)

    print "n_estimators=", variables.n_estimators_et,
    print "max_depth=", variables.max_depth_et,
    print "min_samples_split=", variables.min_samples_split_et,
    print "min_samples_leaf=", variables.min_samples_leaf_et,
    print "max_features=",variables.max_feature_et,
    print "max_leaf_nodes=",variables.max_leaf_nodes_et,
    print "criterion=",variables.criterion_et,
    print "min_impurity_split=",variables.min_impurity_split_et,
    print "class_weight=", variables.cw_et

    prediction_list = clf.predict(test_x)
    prediction_list_prob = clf.predict_proba(test_x)
    return prediction_list,prediction_list_prob
