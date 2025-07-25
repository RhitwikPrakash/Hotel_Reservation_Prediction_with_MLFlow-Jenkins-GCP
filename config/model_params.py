from scipy.stats import randint, uniform

LIGHTGBM_PARAMS = {
    'n_estimators': randint(100, 500),  # Number of boosting iterations
    'max_depth': randint(5, 50),  # Maximum depth of the tree
    'learning_rate': uniform(0.01, 0.2),  # Learning rate
    'num_leaves': randint(20, 100),  # Number of leaves in
    'boosting_type': ['gbdt', 'dart', 'goss'], # Gradient Boosting Decision Tree
}

RANDOM_SEARCH_PARAMS = {
    'n_iter': 6,  # Number of iterations for random search
    'cv': 3,  # Number of cross-validation folds
    'verbose': 2,  # Verbosity level
    'random_state': 42,  # For reproducibility
    'n_jobs': -1,  # Use all available cores of CPU for training
    'scoring': 'accuracy',  # Metric to optimize
}