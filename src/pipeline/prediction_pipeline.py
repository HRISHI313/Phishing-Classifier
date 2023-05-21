import os
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            print("Before Loading")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds

        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self, url: str):
        self.url = url

    def get_data_as_data_frame(self):
        try:
            # Scrape the URL to extract the desired features
            features = self.scrape_url(self.url)

            # Add the URL as a feature
            features["URL"] = self.url

            # Create a DataFrame from the extracted features
            df = pd.DataFrame([features])

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def scrape_url(self, url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"HTTP connection was not successful for the URL: {url}")
                return None
            else:
                soup = BeautifulSoup(response.content, "html.parser")

                # Perform scraping and feature extraction logic here
                features = {
                    'has_title': bool(soup.title),
                    'has_input': bool(soup.find("input")),
                    'has_button': bool(soup.find("button")),
                    'has_image': bool(soup.find("img")),
                    'has_submit': bool(soup.find("input", type="submit")),
                    'has_link': bool(soup.find("a")),
                    'has_password': bool(soup.find("input", type="password")),
                    'has_email_input': bool(soup.find("input", type="email")),
                    'has_hidden_element': bool(soup.find("input", type="hidden")),
                    'has_audio': bool(soup.find("audio")),
                    'has_video': bool(soup.find("video")),
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
                    'has_h1': bool(soup.find("h1")),
                    'has_h2': bool(soup.find("h2")),
                    'has_h3': bool(soup.find("h3")),
                    'length_of_text': len(soup.get_text()) if soup.get_text() else 0,
                    'number_of_clickable_button': len(soup.find_all("button", {"type": ["submit", "button"]})),
                    'number_of_a': len(soup.find_all("a")),
                    'number_of_img': len(soup.find_all("img")),
                    'number_of_div': len(soup.find_all("div")),
                    'number_of_figure': len(soup.find_all("figure")),
                    'has_footer': bool(soup.find("footer")),
                    'has_form': bool(soup.find("form")),
                    'has_text_area': bool(soup.find("textarea")),
                    'has_iframe': bool(soup.find("iframe")),
                    'has_text_input': bool(soup.find("input", type="text")),
                    'number_of_meta': len(soup.find_all("meta")),
                    'has_nav': bool(soup.find("nav")),
                    'has_object': bool(soup.find("object")),
                    'has_picture': bool(soup.find("picture")),
                    'number_of_sources': len(soup.find_all("source")),
                    'number_of_span': len(soup.find_all("span")),
                    'number_of_table': len(soup.find_all("table"))
                }

                return features
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while scraping the URL: {url}\n{str(e)}")
            return None
