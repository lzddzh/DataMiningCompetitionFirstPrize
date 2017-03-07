root_loc = "../original_data/"

# print validation detail option
if_validation_detail = True

# print single validation result
if_display_single_validation_result = True

# write cross validation prediction result
if_write_cv_prediction = True
write_cv_location = "../original_data/prob_train/prediction_with_prob_"

# set CV number 
cv_num = 5 

# set random seed, a given seed will generate specific random numbers
random_seed = 0  # 1234

prob_mode=True

prob_mode = True

######################################### gradient boosting parameters


n_estimators_gdbt = 200
learning_rate_gdbt = 0.1
max_depth_gdbt = 7
min_samples_split_gdbt = 200
min_samples_leaf_gdbt = 250
subsample_gdbt = 1.0
max_feature_gdbt = 'sqrt'

weight_0_gdbt = 1
weight_1000_gdbt = 40
weight_1500_gdbt = 50
weight_2000_gdbt = 90

########################################## AdaBoosting parameters

n_estimators_ada = 350
learning_rate_ada = 0.09

weight_0_ada = 7
weight_1000_ada = 50
weight_1500_ada = 75
weight_2000_ada = 90

# weight_0_ada = 7
# weight_1000_ada = 50
# weight_1500_ada = 75
# weight_2000_ada = 90

########################################## svm parameters

C_svm = 11.0
weight_0_svm = 0.03
weight_1000_svm = 50
weight_1500_svm = 60
weight_2000_svm = 45

########################################## neural network parameters

select_rate_nn = 0.15
unit_num_nn = 1500
learning_rate_init_nn = 0.001
alpha_nn = 0.00003

#########################################  xgboosting parameters

# 0.0268962562551

n_estimators_xgb = 10  # 400
fearning_rate_xgb = 0.14
max_depth_xgb = 3
colsample_bytree_xgb = 0.09
subsample_xgb = 1
min_child_weight_xgb = 1
gamma_xgb = 0
reg_alpha_xgb = 0
reg_lambda_xgb = 1

weight_0_xgb = 2
weight_1000_xgb = 40  # 30
weight_1500_xgb = 60  # 60
weight_2000_xgb = 75  # 90

########################################## gradient boosting blending parameters

n_estimators_gdbt_b = 250
learning_rate_gdbt_b = 0.01
max_depth_gdbt_b = 4
min_samples_split_gdbt_b = 2
min_samples_leaf_gdbt_b = 1
subsample_gdbt_b = 1.0

weight_0_gdbt_b = 0.7
weight_1000_gdbt_b = 5.9
weight_1500_gdbt_b = 8
weight_2000_gdbt_b = 10

########################################## logistic regression parameters

weight_0_lr = 0.9
weight_1000_lr = 5
weight_1500_lr = 7
weight_2000_lr = 9

########################################## Random Forest

n_estimators_rf = 750 
max_depth_rf = 50 
max_leaf_nodes_rf = None 
min_samples_split_rf = 50 
min_samples_leaf_rf = 20 
max_feature_rf = 'sqrt' 
criterion_rf = 'gini'
min_impurity_split_rf = 1e-7
bootstrap_rf = True

weight_0_rf = 4.40 
weight_1000_rf = 59 
weight_1500_rf = 111 
weight_2000_rf = 130 

cw_rf = {"0": weight_0_rf, "1000": weight_1000_rf, "1500": weight_1500_rf, "2000": weight_2000_rf}

########################################## Extra Trees

n_estimators_et = 1000
max_depth_et = 100
max_leaf_nodes_et = None
min_samples_split_et = 60  # 30 - 130
min_samples_leaf_et = 20
max_feature_et = 200  # 23 - 250
criterion_et = 'gini'
min_impurity_split_et = 1e-7
bootstrap_et = False

weight_0_et = 0.035
weight_1000_et = 0.4
weight_1500_et = 0.7
weight_2000_et = 0.85

cw_et = {"0": weight_0_et, "1000": weight_1000_et, "1500": weight_1500_et, "2000": weight_2000_et}

########################################## KNN Bagging 

max_samples_knnBag=0.5
max_features_knnBag=0.5
n_jobs_knnBag=-1
n_estimators_knnBag=10
bootstrap_knnBag=True
bootstrap_features_knnBag=False

