import pandas as pd
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


random_state_dict = {'temp':44,'train':44,'model':44}

# Load the dataset
df = pd.read_csv('/opt/airflow/data/modified/spotify_etl_data.csv')

use_cols = ['mood_score', 'acousticness_%', 'liveness_%', 'speechiness_%',
            'date','in_deezer_playlists', 'in_spotify_playlists', 'in_apple_playlists','bpm','popularity_score']
df.drop([col for col in df.columns.tolist() if col not in use_cols],axis=1,inplace=True)
df.dropna(subset=['popularity_score'],inplace=True)

# Separate target (y) from features (X)
y = df.pop('popularity_score')
X = df
# Train-test split
X_train_temp, X_test, y_train_temp, y_test = train_test_split(
    X, y,
    stratify=y,
    test_size=0.25,
    random_state=random_state_dict['temp']
)
# Second split: separate validation set
X_train, X_val, y_train, y_val = train_test_split(
    X_train_temp, y_train_temp,
    stratify=y_train_temp,
    test_size=0.15,
    random_state=random_state_dict['train']
)

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
    'model__n_estimators': [200,300,400],
    'model__max_depth': [20,40],
    'model__min_samples_split': [3,4],
    'model__min_samples_leaf': [3,4],    
    'model__max_features': [0.5,0.6,0.75]
}
# Create GridSearchCV with the pipeline
grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1,
    verbose=1
)

# Fit the grid search
grid_search.fit(X_train, y_train)



# Get best parameters and score
print("Best parameters:", grid_search.best_params_)
print("Best cross-validation score:", grid_search.best_score_)

# Get the best model from grid search
best_model = grid_search.best_estimator_
#best_model.fit(X_train, y_train) redundant

for i,c in zip(best_model.named_steps['model'].feature_importances_,
               best_model.named_steps['preprocessor'].transformers_[0][2]):
    print(i,c)

# Make predictions
predictions = best_model.predict(X_test)

# Print some evaluation metrics
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
