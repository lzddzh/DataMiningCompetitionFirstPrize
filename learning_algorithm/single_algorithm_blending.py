from sklearn.ensemble import GradientBoostingClassifier
from commons import variables
from commons import tools
from scipy.stats import mode


def learn(x, y, test_x):
    prediction_list = []
    for pred_list in test_x:
        prediction_list.append(str(int(pred_list[4])))

    return prediction_list
