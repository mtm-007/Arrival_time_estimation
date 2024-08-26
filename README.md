# Arrival_time_estimation

#### Using Anaconda3 2022 
- This specific version of anaconda is used here
- wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh

## Data source
- Instead of shuffling the data set they are to be used as chronologically ordered dataset
- The data is collected from Nyc taxi records, 2023 records are selected
- In the earlier stages -> Jan is used for Training
                        -> Feb is used for validation
                        -> Mar is used for Testing
- Later most of the data (Jan to Sep) data records will be used for Training, the rest for Validation and Testing. Alternatively the latest 2024 records can be added.

## Experimental Tracking and Model Management
- Mlflow is ustilied for Experiments Tracking and model management as its widely available open source workflow tool.

# Hyperparameter Tuning 
- Hyperopt library is used for hyper parameter tuning[Bayesian based] 