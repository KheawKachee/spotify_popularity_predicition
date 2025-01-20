import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
df = pd.read_csv('data/modified/spotify_etl_data.csv')

# Clean the data
df.drop('streams', axis=1, inplace=True)
df.dropna(subset=['popularity_score', 'in_shazam_charts'], inplace=True)

# Separate target (y) from features (X)
y = df.pop('popularity_score')
X = df

# Define text and numeric columns
text_cols = ['track_name', 'artist(s)_name']
numeric_cols = [col for col in X.columns if col not in text_cols]

# Set up the column transformer with separate TfidfVectorizer for each text column
preprocessor = ColumnTransformer(
    transformers=[
        (f"text_{col}", TfidfVectorizer(max_features=100), col) for col in text_cols
    ] + [
        ("numeric", StandardScaler(), numeric_cols)
    ],
    remainder='drop'  # Drop any columns not specified
)

# Set up the pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LinearRegression())
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y,stratify=y, test_size=0.25, random_state=1)
# Remove stratify=y as it might cause issues with continuous target variable

# Train the pipeline
pipeline.fit(X_train, y_train)

# Make predictions
predictions = pipeline.predict(X_test)

# Print some evaluation metrics
print("Mean Squared Error:", mean_squared_error(y_test, predictions))
print("R2 Score:", r2_score(y_test, predictions))