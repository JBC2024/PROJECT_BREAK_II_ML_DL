import os
import variables as vrb
import general as grl

import numpy as np
import pandas as pd
import pickle

# -----------------------------------------------------
# -------------------- OS Methods  --------------------
# -----------------------------------------------------
def exist_file(filename):
    """
    Check if file exists. Return 'True' if file exists

    Args:
    filename (str): Filename to check
   """

    return os.path.exists(filename)

# -------------------------------------------------------
# -------------------- Data Methods  --------------------
# -------------------------------------------------------
def read_data(path=vrb.DATASOURCE_PATH):
    df = pd.read_csv(path, parse_dates=[vrb.COLUMN_DATE_ORIGINAL], index_col=vrb.COLUMN_DATE_ORIGINAL)
    return df

# -----------------------------------------------------------
# -------------------- Fit Info Methods  --------------------
# -----------------------------------------------------------
def save_fit_info(df):
    df.to_csv(vrb.FIT_RESULTS_PATH, index=False)

def read_fit_info_dataset():
    if not exist_file(vrb.FIT_RESULTS_PATH):
        df_info = pd.DataFrame({}, columns=vrb.COLUMNS_INFO_ARRAY)
        save_fit_info(df_info)
    
    df_info = pd.read_csv(vrb.FIT_RESULTS_PATH, parse_dates=[vrb.INFO_COLUMN_START_DATE, vrb.INFO_COLUMN_FINISH_DATE])
    return df_info

def add_fit_info(model_name, model_state, columns, start_time, total_epochs, epochs_completed, valid_loss, valid_mae, valid_rmse):
    dt_now = grl.get_datetime()
    total = dt_now - start_time
    
    new_row = {vrb.INFO_COLUMN_NAME: model_name,
               vrb.INFO_COLUMN_FEATURES_TPYE: grl.get_features_type(columns), 
               vrb.INFO_COLUMN_STATE: model_state,
               vrb.INFO_COLUMN_COLUMNS: str(columns),
               vrb.INFO_COLUMN_START_DATE: start_time,
               vrb.INFO_COLUMN_FINISH_DATE: dt_now,
               vrb.INFO_COLUMN_TOTAL_TIME: total,
               vrb.INFO_COLUMN_EPOCHS_CONFIG: total_epochs, 
               vrb.INFO_COLUMN_EPOCHS_COMPLETED: epochs_completed,
               vrb.INFO_COLUMN_VALID_LOSS: valid_loss,
               vrb.INFO_COLUMN_VALID_MAE: valid_mae,
               vrb.INFO_COLUMN_VALID_RMSE: valid_rmse
               }
    df_fit = read_fit_info_dataset()
    df_fit.loc[len(df_fit)] = new_row
    save_fit_info(df_fit)
    return df_fit


# --------------------------------------------------------
# -------------------- Model Methods  --------------------
# --------------------------------------------------------
def get_model_name(filename):
    return f"{vrb.SAVED_MODELS_DIRECTORY}{filename}.pkl"

def read_model(filename):
    loaded_model = None
    if exist_file(get_model_name(filename)):
        with open(get_model_name(filename), 'rb') as file:
            loaded_model = pickle.load(file)
    return loaded_model
    
def save_model(model, filename):
    with open(get_model_name(filename), 'wb') as file:
        pickle.dump(model, file)