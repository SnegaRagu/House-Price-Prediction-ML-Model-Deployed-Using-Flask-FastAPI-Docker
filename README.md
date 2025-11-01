# House-Price-Prediction-ML-Model-Deployed-Using-Flask-FastAPI-Docker

The House Price Prediction project focuses on predicting real estate prices using machine learning models. The model is trained on historical Banglore housing data to estimate property prices based on various features like location, size, and amenities. The deployment is achieved through Flask and FastAPI frameworks for web-based interaction, with Docker ensuring easy containerization and portability of the application.

## Project Overview

### 1. Problem Understanding

> The goal is to predict real estate price based on features using ML models and deploy it via Flask and FastAPI frameworks for browser based interactions and containerize with Docker to ease access.
> The features involving in house price prediction are area type, availability, location, size, total square feet, bath and balcony.
  [Bengaluru House Price Dataset](https://www.kaggle.com/datasets/sumanbera19/bengaluru-house-price-dataset)

### 2. Data Preprocessing

> 1. Load Dataset
> 2. EDA
> 3. Feature and Target Selection
> 4. Train-Test-Split
> 5. Pre-processing Pipeline [Impute -> FunctionalTransformer(as needed) -> Encoding or Scaling]

### 3. Model Training

> Creating Model pipeline with preprocessor and machine learning model.
> ML models used to predict prices are

  1. Linear Regression
  2. Polynomial Regression [Polynomial features enabled on numeric data]
  3. Random Forest + Hyperparameter Tuning with GridSearchCV
  4. XGBoost + Hyperparameter Tuning with GridSearchCV

> Saving the best models of each Ml algorithms for Flask and FastAPI deployment.

### 4. Model Evaluation

> All four ML models been evaluated with RMSE and R2 score values.

### 5. Building Flask API for house 

> Created 2 GET routes, one for home page and other for Model info page.
> Created POST route to evaluate and predict the house price of any given input features for 4 models mentioned above using Flask.
> Tested results using Postman and displayed results in JSON format.
> Directory structure of Flask API

  house-price-flaskapi-app/
  
  ├── app.py
  
  ├── models/
  
  │   ├── RandomForest.pkl
  
  │   ├── linear_regression.pkl
  
  │   ├── polynomial_regression.pkl
  
  │   ├── XGBoost.pkl
  
  ├── requirements.txt
  
  ├── custom_functions.py

> To run Flask API, run as below inside Flask API directory

> python app.py

### 6. Building FastAPI and Containerize with Docker

> Created 2 GET results, one for home and other for Model Info.
> Created POST route to evaluate and predict the house price of any given input features for 4 models mentioned above using FastAPI.
> Containerized the entire app data into docker by copying local files into container, installing necessary dependencies and starting FastAPI inside the container.
> Running the Docker container gives interactive web browser with model prediction prices.
> Directory structure of FastAPI

  house-price-fastapi-app/
  
  ├── app/
  
  │   ├── main.py
  
  │   ├── utils.py
  
  │   ├── schema.py
  
  │   ├── model.py
  
  ├── models/
  
  │   ├── RandomForest.pkl
  
  │   ├── linear_regression.pkl
  
  │   ├── polynomial_regression.pkl
  
  │   ├── XGBoost.pkl
  
  ├── requirements.txt
  
  ├── Dockerfile

To run FastAPI only,  run as below inside Flask API directory

> uvicorn app.main:app --reload
> Accessible at http://127.0.0.1:8000/docs --> Swagger UI (interactive API tester)

To run Docker install wsl and Docker Desktop and follow the below steps in flaskapi root directory:

> 1. Rebuilding Docker image >>>>> docker build -t house-price-app .
> 2. Run Docker Container    >>>>> docker run -d -p 8000:8000 house-price-app
> 3. Access at               >>>>> http://localhost:8000/docs
