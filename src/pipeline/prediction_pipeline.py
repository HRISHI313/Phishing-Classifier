import sys
import os
import requests
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
from src.logger import logging

import requests
from bs4 import BeautifulSoup

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,df):
        logging.info('Logging 1')
        try:
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            data_scaled = preprocessor.transform(df)
            preds = model.predict(data_scaled)
            return preds

            logging.info('logging-2')

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    logging.info("Logging -3")
    def __init__(self,url:str):
        self.url = url

    def get_data_as_data_frame(self):
        logging.info("Logging -4")
        try:
            # Scrape the URL to extract the desired features
            features = self.scrape_url(self.url)


            # Convert boolean features to 1 or 0
            converted_features = {key: int(value) for key, value in features.items() if isinstance(value, bool)}


             # Create a DataFrame from the converted features
            df = pd.DataFrame([converted_features])

            return df
            logging.info("Logging -5")

        except Exception as e:
            raise CustomException(e, sys)

    def scrape_url(self, url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                logging.error(f"HTTP connection was not successful for the URL: {url}")
                return None

            soup = BeautifulSoup(response.content, "html.parser")
            features = {
                'has_title': int(bool(soup.title)),
                'has_input': int(bool(soup.find("input"))),
                'has_button': int(bool(soup.find("button"))),
                'has_image': int(bool(soup.find("img"))),
                'has_submit': int(bool(soup.find("input", type="submit"))),
                'has_link': int(bool(soup.find("a"))),
                'has_password': int(bool(soup.find("input", type="password"))),
                'has_email_input': int(bool(soup.find("input", type="email"))),
                'has_hidden_element': int(bool(soup.find("input", type="hidden"))),
                'has_audio': int(bool(soup.find("audio"))),
                'has_video': int(bool(soup.find("video"))),
                'number_of_inputs': len(soup.find_all("input")),
                'number_of_buttons': len(soup.find_all("button")),
                'number_of_images': len(soup.find_all("img")),
                'number_of_option': len(soup.find_all("option")),
                'number_of_list': len(soup.find_all("li")),
                'number_of_th': len(soup.find_all("th")),
                'number_of_tr': len(soup.find_all("tr")),
                'number_of_href': len(soup.find_all(href=True)),
                'number_of_paragraph': len(soup.find_all("p")),
                'number_of_script': len(soup.find_all("script")),
                'length_of_title': len(soup.title.string) if soup.title and soup.title.string else 0,
                'has_h1': int(bool(soup.find("h1"))),
                'has_h2': int(bool(soup.find("h2"))),
                'has_h3': int(bool(soup.find("h3"))),
                'length_of_text': len(soup.get_text()) if soup.get_text() else 0,
                'number_of_clickable_button': len(soup.find_all("button", {"onclick": True})),
                'number_of_a': len(soup.find_all("a")),
                'number_of_img': len(soup.find_all("img")),
                'number_of_div': len(soup.find_all("div")),
                'number_of_figure': len(soup.find_all("figure")),
                'has_footer': int(bool(soup.find("footer"))),
                'has_form': int(bool(soup.find("form"))),
                'has_text_area': int(bool(soup.find("textarea"))),
                'has_iframe': int(bool(soup.find("iframe"))),
                'has_text_input': int(bool(soup.find("input", type="text"))),
                'number_of_meta': len(soup.find_all("meta")),
                'has_nav': int(bool(soup.find("nav"))),
                'has_object': int(bool(soup.find("object"))),
                'has_picture': int(bool(soup.find("picture"))),
                'number_of_sources': len(soup.find_all("source")),
                'number_of_span': len(soup.find_all("span")),
                'number_of_table': len(soup.find_all("table")),
            }

            return features

        except Exception as e:
            logging.error(f"An error occurred while scraping the URL: {e}")
            raise CustomException(e)

# has_title,has_input,has_button,has_image,has_submit,has_link,has_password,has_email_input,has_hidden_element,\
#     has_audio,has_video,number_of_inputs,number_of_buttons,number_of_images,number_of_option,number_of_list,\
#     number_of_th,number_of_tr,number_of_href,number_of_paragraph,number_of_script,length_of_title,has_h1,has_h2,\
#     has_h3,length_of_text,number_of_clickable_button,number_of_a,number_of_img,number_of_div,number_of_figure,\
#     has_footer,has_form,has_text_area,has_iframe,has_text_input,number_of_meta,has_nav,has_object,has_picture,\
#     number_of_sources,number_of_span,number_of_table






