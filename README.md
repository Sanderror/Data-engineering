# Data-engineering

## How to run the code?
The serving application can be ran using a Virtual Machine or using Cloud Run, with the constraint that one has added all the required files to the Cloud Storage buckets, has created and built all the Docker images and containers, and has created all the triggers.

## Meaning of files
### prediction-ui folder
This folder contains the UI components of the serving application
* The Dockerfile was used to create the Docker image
* The templates folder contains the input_page.html and the response_page.html what is displayed to the user when using the app
* The app.py file was used to process the input link from the user into data variables, request the API to make a prediction, and then output the response_page.html according to the output of the prediction

### prediction-api folder
This folder contains the API components of the serving application
* The Dockerfile was used to create the Docker image
* The phishing_predictor.py file was used to create the prediction on the input data from the UI component
* The app.py file was used to get the prediction of phishing_predictor.py on the data and push it back to UI component

### data folder
Contains the datasets used in the application
* The Phishing_Legitimate_full.csv file is the original dataset as obtained from Kaggle (https://www.kaggle.com/datasets/shashwatwork/phishing-dataset-for-machine-learning)
* The phishing.csv file is the dataset used in the Cloud Storage, which has been used throughout the application, on which the model was also trained

### pipeline_creation_phishing_final.ipynb file
The notebook which contains the ML pipeline that was run in Vertex AI
* Loads the data from Cloud Storage
* Splits the data into a train and test set
* Trains and calculates performance of 3 classification models: SVM, RF, LR
* Compares the models and chooses the best model based on recall (with an accuracy of at least 0.7)
* Uploads the chosen model to Cloud Storage
* Triggers the trigger for service redeployment (which uses configuration file service_deployment_cloudbuild.json, see below)
* Compiles the ML pipeline into the phishing_predictor_training_pipeline_final.yaml file

### phishing_predictor_training_pipeline_final.yaml file
ML pipeline compiled in a .yaml file as created in pipeline_creation_phishing_final.ipynb

### service_deployment_cloudbuild.json file
The cloudbuild configuration file to be able to run Cloud Build triggers that redeploy the serving app
* Copies the model from the model bucket in Cloud Storage
* Builds the Docker images for the prediction-ui and prediction-api components
* Pushes the images to the Artifact Registry
* Creates containers for deployment in Cloud Run (automatically connects the prediction-ui and prediction-api containers with each other)

### pipeline_executor folder
Folder to create an executor of the ML pipeline (for continuous retraining)
* The Docker file was used to create a Docker image
* The pipeline_executor.py parses the necessary arguments into the pipeline job, to be able to retrain it consistently

### phishing_executor_tool_cloudbuild.json file
The cloudbuild configuration file to create the pipeline_executor image
* Build the Docker image for the pipeline_executor
* Pushes the image to the Artifact Registry

### phishing_predictor_pipeline_execution_cloudbuild.json file
The cloudbuild configuration file to be able to retrain the ML pipeline when desired
* Copies the parameters for the ML pipeline from the data bucket in Cloud Storage
* Runs the pipeline_executor image using the yaml file of the compiled ML pipeline, and the parameters

### other folder
Contains extra objects related to the project
* The DataCleaning.ipynb file contains the process of how we obtained the phishing.csv dataset from the original Phishing_Legitimate_full.csv dataset
* The Final_FlowChart.jpg and Final_Flowchart.pdf are the pictures of the flowcharts of the whole MLOps system
* The Report Assignment 1.pdf file is the report we handed in on Canvas for the assignment
