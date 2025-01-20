# Spotify Song Popularity Predictor

## Overview
This project implements a machine learning model to predict song popularity scores on Spotify using features like track name, artist name, and various audio metrics. The model uses TF-IDF vectorization for text data and standard scaling for numerical features to predict discrete popularity scores (ranging from 4-7).

## Features
- Text feature processing for track names and artist names
- Numerical feature scaling
- Stratified sampling to maintain balanced popularity score distribution
- Pipeline-based implementation using scikit-learn
- Support for both regression and classification approaches

## Prerequisites
- Python 3.9+
- Docker (for development environment)
- Required Python packages:
  - pandas
  - scikit-learn
  - numpy

## Project Structure
spotifyrec/
├── data/
│   └── modified/
│       └── spotify_etl_data.csv
├── ml.py
├── README.md
└── [other project files]
Copy

## Setup

1. Clone the repository:
    ```bash
    git clone [repository-url]
    cd spotifyrec
    ```

2. Using Docker (recommended):
    ```bash
    docker-compose up -d
    ```

   Or set up a local environment:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main script:
    ```bash
    python ml.py
    ```

The script will:
1. Load and preprocess the Spotify dataset
2. Train a model on the processed data
3. Output prediction metrics including MSE, R² score, and accuracy

## Data Description
The dataset (`spotify_etl_data.csv`) includes:

- Track name
- Artist(s) name
- Popularity score (target variable, discrete values 4-7)
- Various audio features and metrics
- Shazam charts presence indicator

## Model Details

- **Text features**: TF-IDF Vectorization (max_features=100)
- **Numeric features**: Standard Scaling
- **Current implementation**: Linear Regression with rounded predictions
- **Stratified sampling** for balanced class distribution

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
[Insert your chosen license here]

## Acknowledgments
- Spotify Web API for providing the data infrastructure
- scikit-learn for machine learning tools
