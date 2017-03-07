from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from commons import variables
from commons import tools
from scipy.stats import mode


def learn(x, y, test_x):
    clf = BaggingClassifier(KNeighborsClassifier(1, 'distance'),
                                                max_samples=variables.max_samples_knnBag,
                                                max_features=variables.max_features_knnBag,
                                                n_jobs=variables.n_jobs_knnBag,
                                                n_estimators=variables.n_estimators_knnBag,
                                                bootstrap=variables.bootstrap_knnBag,
                                                bootstrap_features=variables.bootstrap_features_knnBag,
                                                random_state=variables.random_knnBag
                                                ).fit(x, y)

    prediction_list = clf.predict(test_x)
    return prediction_list
