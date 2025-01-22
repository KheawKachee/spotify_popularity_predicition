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
