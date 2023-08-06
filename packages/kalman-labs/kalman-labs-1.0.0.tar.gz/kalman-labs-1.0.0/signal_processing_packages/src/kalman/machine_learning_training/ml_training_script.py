from signal_processing_packages.src.kalman.audio_features.extract_features import generate_feature_file
# from sklearn.ensemble import RandomForestClassifier

# def select_ml_model(ml_model, path):
#
#     model_path = ""
#
#     if ml_model == "random_forest":
#         model_path = train_random_forest_model(path)
#
#     elif ml_model == "svm":
#         model_path = train_svm_model(path)
#
#     elif ml_model == "decision_tree":
#         model_path = train_decision_tree_model(path)
#
#     elif ml_model == "xgboost":
#         model_path = train_xgboost_model(path)
#
#
#     return model_path
#
#
#
# def train_random_forest_model(path):
#     audio_df = generate_feature_file(path)
#     y_train = audio_df['label']
#     x_train = audio_df.drop(columns = ['label'])
#     model_rf = RandomForestClassifier(n_estimators=201, criterion="entropy")
#     model_rf.fit(x_train, y_train)
#
#
#
#
#
#
#
#
# def train_svm_model():
#
#
#
#
#
#
#
# def train_decision_tree_model():
#
#
#
#
#
#
#
# def train_xgboost_model():
#
