# Holiday Recommendation System Using Markov Chains

A Markov chain-based recommendation system for Indonesian tourism destinations that combines probabilistic modeling with collaborative and content-based filtering to provide personalized travel recommendations.

**Academic Project**: Uppsala University - Artificial Intelligence (1DL340) - HT2023

**Authors**: Gabrielle Fidelis de Castilho, Hemavathi Hanasoge Siddaiah, Kim Kuruvilla Mathews

## Overview

This project implements a recommendation system that suggests tourist attractions based on user visit history, age demographics, spending patterns, and destination ratings. The system uses Markov chains to model category transition probabilities, capturing the likelihood of users moving from one type of attraction to another, combined with collaborative filtering to rank specific destinations.

## Key Features

- **Markov Chain Category Prediction**: Models transitions between attraction categories (Culture, Amusement Park, Natural Reserve, etc.)
- **Age-Based Collaborative Filtering**: Recommends attractions highly rated by users in similar age ranges
- **Budget-Aware Recommendations**: Filters suggestions based on user's historical spending patterns (within 2x average)
- **Visit History Tracking**: Ensures only new, unvisited attractions are recommended
- **Multi-City Support**: Works across Jakarta, Yogyakarta, Semarang, Bandung, and Surabaya
- **Cold Start Handling**: Provides equal probability recommendations for new users without history

## Dataset

The system uses the [Indonesia Tourism Destination dataset](https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination/data) from Kaggle, containing:

- **437 tourist attractions** across 5 major Indonesian cities
- **300 users** with demographic information (age, location)
- **10,000 user ratings** for various destinations

## Installation

### Prerequisites
```bash
Python 3.7+
```

### Required Libraries:
```bash
pip install pandas numpy scikit-learn
```

## Project Structure

```
markov_tourism_recommendation/
├── main.py                          # Main recommendation system
├── documentation.py                 # Function documentation
├── test_recommendations.py          # Basic functionality tests
├── test_accuracy.py                 # Accuracy validation tests
├── data_preprocessing.ipynb         # Data preprocessing notebook
├── ai_project_report.pdf            # Full academic report
└── README.md                        # This file
```

## Usage

### Running the Recommendation System

```bash
python main.py
```

The program prompts for:
1. **User ID** (1-300, or enter a new ID for cold start scenario)
2. **Current Category** (the category the user is currently viewing)
3. **City** (the city where recommendations are needed)

### Example Session

```
Add User ID (1 to 300): 15
Add Category (Culture, Amusement Park, Natural Reserve, Nautical, Place of Worship, Shopping Center): Culture
Add City (Jakarta, Bandung, Surabaya, Yogyakarta, Semarang): Jakarta

Category Recommended:
Natural Reserve

Top Recommendations:
{123: 'Ragunan Zoo', 145: 'Thousand Islands', 89: 'Ancol Beach', 201: 'Taman Mini Indonesia', 156: 'Pulau Seribu Marine Park'}
```

## Documentation

Complete academic documentation including methodology, results, analysis, and references is available in:
- **[ai_project_report.pdf](ai_project_report.pdf)** - Full project report (14 pages)
- **[documentation.py](documentation.py)** - Comprehensive function documentation with usage examples
- **[data_preprocessing.ipynb](data_preprocessing.ipynb)** - Exploratory data analysis
- Dataset provided by [Aprabowo on Kaggle](https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination/data)
- Course instructors at Uppsala University Department of Information Technology
- Research foundations from Ricci et al. and Liu et al. on recommender systems
