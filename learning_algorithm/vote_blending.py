from sklearn.ensemble import GradientBoostingClassifier
from commons import variables
from commons import tools
from scipy.stats import mode


def get_vote_weight(algorithm):
    # ["gdbt", "ada", "svm", "rf", "et","xgb","nn"]

    if algorithm == 0:
        return 0
    elif algorithm == 1:
        return 2
    elif algorithm == 2:
        return 0
    elif algorithm == 3:
        return 1
    elif algorithm == 4:
        return 2
    elif algorithm == 5:
        return 0
    elif algorithm == 6:
        return 0



def learn(x, y, test_x):
    prediction_list = []
    for pred_list in test_x:
        pred_dict = {}
        for i in range(len(pred_list)):
            if pred_dict.has_key(pred_list[i]):
                pred_dict[pred_list[i]] += get_vote_weight(i)
            else:
                pred_dict[pred_list[i]] = get_vote_weight(i)

        pred_dict_list = sorted(pred_dict.iteritems(), key=lambda d: d[1], reverse=True)

        prediction_list.append(str(int(pred_dict_list[0][0])))

    return prediction_list
