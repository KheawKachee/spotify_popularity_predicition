import pandas as pd
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score


random_state_dict = {'temp':44,'train':44,'model':44}

# Load the dataset
df = pd.read_csv('data/modified/spotify_etl_data.csv')

# Clean the data
drop_cols =['track_name', 'artist(s)_name', 'streams']
df.drop(drop_cols, axis=1, inplace=True)
df.dropna(subset=['popularity_score', 'in_shazam_charts'], inplace=True)

# Separate target (y) from features (X)
y = df.pop('popularity_score')
X = df

# Train-test split
X_train_temp, X_test, y_train_temp, y_test = train_test_split(
    X, y,
    stratify=y,
    test_size=0.2,
    random_state=random_state_dict['temp']
)
#print(X_train_temp,y_train_temp)

# Second split: separate validation set 
X_train, X_val, y_train, y_val = train_test_split(
    X_train_temp, y_train_temp,
    stratify=y_train_temp,
    test_size=0.2,
    random_state=random_state_dict['train']
)
# Remove stratify=y as it might cause issues with continuous target variable

# Set up the column transformer with separate TfidfVectorizer for each text column
preprocessor = ColumnTransformer(
    transformers=[("numeric", StandardScaler(), df.columns)],
    remainder='drop'
)

# Create the pipeline with preprocessing and model
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(random_state=random_state_dict['model']))
])

# Define parameter grid
param_grid = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [10, 15],
    'model__min_samples_split': [2, 3, 5],
    'model__min_samples_leaf': [2, 3, 5],    
    'model__max_features': [0.4, 0.5]
}

# Create GridSearchCV with the pipeline
grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=10,
    scoring='r2',
    n_jobs=-1,
    verbose=1
)


def do_grid_search(X_train, y_train, X_val, y_val):
    # Fit the grid search
    grid_search.fit(X_train, y_train)
    
    # Get best parameters and score
    print("Best parameters:", grid_search.best_params_)
    print("Best cross-validation score:", grid_search.best_score_)
    
    # Get the best model from grid search
    best_model = grid_search.best_estimator_
    
    '''
    # Evaluate on validation set
    val_score = best_model.score(X_val, y_val)
    print("Validation set score:", val_score)
    
    # Evaluate on test set
    test_score = best_model.score(X_test, y_test)
    print("Test set score:", test_score)
    '''
    
    return best_model


def do_prediction(X_train, y_train,X_test, y_test):
    # Train the pipeline
    pipeline.fit(X_train, y_train)

    # Make predictions
    predictions = pipeline.predict(X_test)

    # Print some evaluation metrics
    print("Mean Squared Error:", mean_squared_error(y_test, predictions))
    print("R2 Score:", r2_score(y_test, predictions))


# Run 
best_model = do_grid_search(X_train, y_train, X_val, y_val)
do_prediction(X_train, y_train,X_test, y_test)