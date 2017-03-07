from sklearn.ensemble import GradientBoostingClassifier
from commons import variables
from commons import tools
from scipy.stats import mode
import numpy
#import xgboost


def learn(x, y, test_x):
    # set sample weight


    weight_list = []
    for j in range(len(y)):
        if y[j] == "0":
            weight_list.append(variables.weight_0_xgb)
        if y[j] == "1000":
            weight_list.append(variables.weight_1000_xgb)
        if y[j] == "1500":
            weight_list.append(variables.weight_1500_xgb)
        if y[j] == "2000":
            weight_list.append(variables.weight_2000_xgb)

#    clf = xgboost.XGBClassifier(objective="multi:softmax", max_depth=variables.max_depth_xgb,
#                                learning_rate=variables.learning_rate_xgb, n_estimators=variables.n_estimators_xgb,
#                                colsample_bytree=variables.colsample_bytree_xgb, subsample=variables.subsample_xgb,
#                                min_child_weight=variables.min_child_weight_xgb, gamma=variables.gamma_xgb,
#                                seed=variables.random_seed, reg_alpha=variables.reg_alpha_xgb,
#                                reg_lambda=variables.reg_lambda_xgb).fit(numpy.asarray(x), numpy.asarray(y),
#                                                                         numpy.asarray(weight_list))
#    prediction_list = clf.predict(test_x)
#    prediction_list_prob = clf.predict_proba(test_x)
    # print prediction_list_prob
    # print clf.classes_

    return prediction_list, prediction_list_prob
