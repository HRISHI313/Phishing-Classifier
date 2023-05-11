import os
import sys

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer

@dataclass
class datatranformer_config:
    preprocessor_obj_file_path =os.path.join('artifacts','preprocessor.pkl')

class data_transformer:
    def __init__(self):
        self.datatransformer_config = datatranformer_config()

    def get_data_transformer_object(self):
        logging.info('Missing value and Duplicated removing initiated')
        try:
            columns=['has_title','has_input','has_button','has_image','has_submit','has_link',
                    'has_password','has_email_input','has_hidden_element','has_audio',
                    'has_video','number_of_inputs','number_of_buttons','number_of_images',
                    'number_of_option','number_of_list','number_of_th','number_of_tr',
                    'number_of_href','number_of_paragraph','number_of_script',
                    'length_of_title','has_h1','has_h2','has_h3','length_of_text',
                    'number_of_clickable_button','number_of_a','number_of_img',
                    'number_of_div','number_of_figure','has_footer','has_form',
                    'has_text_area','has_iframe','has_text_input','number_of_meta',
                    'has_nav','has_object','has_picture','number_of_sources','number_of_span',
                    'number_of_table']

            pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')),
                                       ('Standard_scalar',StandardScaler())])
            logging.info('Removing duplicate and missing values completed')

            preprocessor = ColumnTransformer([('pipeline',pipeline,columns)])
            logging.info('Missing value and Duplicated removing completed')

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformer(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Reading train and test data completed")

            logging.info('Obtaining preprocessor object')
            preprocessor_obj = self.get_data_transformer_object()

            feature_column = 'has_title','has_input','has_button','has_image','has_submit','has_link','has_password',\
                'has_email_input','has_hidden_element','has_audio','has_video','number_of_inputs',\
                'number_of_buttons','number_of_images','number_of_option','number_of_list','number_of_th',\
                'number_of_tr','number_of_href','number_of_paragraph','number_of_script','length_of_title',\
                'has_h1','has_h2','has_h3','length_of_text','number_of_clickable_button','number_of_a',\
                'number_of_img','number_of_div','number_of_figure','has_footer','has_form','has_text_area',\
                'has_iframe','has_text_input','number_of_meta','has_nav','has_object','has_picture',\
                'number_of_sources','number_of_span','number_of_table'

            input_feature_train_df = train_df[list(feature_column)]
            target_feature_train_df = train_df['label']

            input_feature_test_df = test_df[list(feature_column)]
            target_feature_test_df = test_df['label']


            logging.info('Applying preprocessing object on training dataframe and testing dataframe')

            # fit_transform on training set
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]

            # transform on test set
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # Save Preprocessing object
            logging.info('Saving Preprocessing object')
            save_object(self.datatransformer_config.preprocessor_obj_file_path,
                        obj=preprocessor_obj)
            logging.info('Saved Preprocessing object')

            return (train_arr,
                    test_arr)


        except Exception as e:
            raise CustomException (e,sys)


