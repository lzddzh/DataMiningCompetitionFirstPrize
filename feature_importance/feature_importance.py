from sklearn.ensemble import GradientBoostingClassifier
from commons import tools
from commons import variables

training_file_loc = "../original_data/training_examples.txt"
output_file_loc = "../original_data/important_features.txt"
w = open(output_file_loc, 'w')

x = []
y = []

tools.read_data_with_label([training_file_loc], x, y, None, None)
(x, y) = tools.simple_negative_sample(x, y, variables.select_rate)

clf = GradientBoostingClassifier(loss='deviance', n_estimators=variables.n_estimators_gdbt,
                                 learning_rate=variables.learning_rate_gdbt,
                                 max_depth=variables.max_depth_gdbt, random_state=variables.random_seed,
                                 min_samples_split=variables.min_samples_split_gdbt,
                                 min_samples_leaf=variables.min_samples_leaf_gdbt,
                                 subsample=variables.subsample_gdbt,
                                 max_features=variables.max_feature_gdbt).fit(x, y)

# feature importance
name_list = []
lines = open(variables.root_loc + "collumInfo.txt")
for line in lines:
    name_list.append(line.strip("\n").split("    ")[2])

importance_list = clf.feature_importances_
impor_dict = {}
for i in range(len(importance_list)):
    impor_dict[i] = importance_list[i]

impor_dict_list = sorted(impor_dict.iteritems(), key=lambda d: d[1], reverse=True)

for i in range(len(impor_dict_list)):
    print "fea" + str(impor_dict_list[i][0]) + " " + str(name_list[impor_dict_list[i][0]]) + " : " + str(
        impor_dict_list[i][1])

for i in range(len(impor_dict_list)):
    w.write(str(impor_dict_list[i][0]) + "\n")

w.close()
