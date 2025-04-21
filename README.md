# housing-prices-ml-model
A machine learning-based system to predict residential property prices using publicly available housing data, primarily focused on the Seattle market.

## Overview
This project involves developing a machine learning model to predict real estate housing prices using publicly available datasets. The model primarily utilizes a random forest regression algorithm to input different independent variables to help stakeholders estimate the price of the proprety.

## Problem Statement
Traditional methods for predicting real estate sale prices have become outdated and insufficient, often neglecting many important factors and leading to inconsistent or inaccurate pricing. Our project aims to improve that prediction accuracy and enable stakeholders to make better-informed decisions.

## Purpose
The purpose of this model is to utilize machine learning techniques to identify patterns in property market data and produce more accurate predictions than traditional methods. The model can be expanded and continuously improved by incorporating new datasets and additional variables, enhancing its predictive accuracy of the price of the property over time. 

## Data Sources
The dataset includes publicly available Seattle real estate data:
- `Housing_Seattle_2014_15.csv` – Historical housing data.
- `housing_cleaned.csv` – Cleaned dataset ready for ML modeling.
- `housing_price_inputs.csv` – Sample inputs for predictions.

## System Diagram & Data Pipeline
1. Data Acquisition: Obtained public real estate data.
2. Preprocessing: Cleaning, handling missing values, and feature scaling.
3. Modeling: Random Forest Regression.
4. Evaluation: RMSE, MAE, MAPE metrics.
5. Deployment: Model served via Streamlit and FastAPI applications.

## Running the Project

### Requirements
- Python 3.x
- pandas
- numpy
- scikit-learn
- fastapi
- streamlit
- mlflo
- uvicorn

Install dependencies:
```bash
pip install -r requirements.txt
