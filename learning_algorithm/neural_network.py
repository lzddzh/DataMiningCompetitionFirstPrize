from sklearn.neural_network import MLPClassifier
from commons import variables
from commons import tools
from scipy.stats import mode


def learn(x, y, test_x):
    (temp_x, temp_y) = tools.simple_negative_sample(x, y, variables.select_rate_nn)

    clf = MLPClassifier(hidden_layer_sizes=(variables.unit_num_nn,), random_state=2017, max_iter=2000,
                        alpha=variables.alpha_nn,
                        learning_rate_init=variables.learning_rate_init_nn,solver="adam",activation="relu").fit(temp_x, temp_y)
    prediction_list = clf.predict(test_x)
    prediction_list_prob = clf.predict_proba(test_x)

    return prediction_list,prediction_list_prob
