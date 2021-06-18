# Other Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext.markdown import Markdown

# Google Map
from flask_googlemaps import GoogleMaps

# Tech Crunch Scraper

import bs4
import requests
import pandas as pd
import xlsxwriter

class ScrapeNews():
    def auto_adjust_excel_columns(self, worksheet, df):
        for idx, col in enumerate(df):
            series = df[col]
            max_len = (
                max(
                    (
                        series.astype(str).map(len).max(),
                        len(str(series.name)),
                    )
                )
                + 1
            )
            worksheet.set_column(idx, idx, max_len)

    def scrape(self):
        url = "https://techcrunch.com/"
        response = requests.get(url)

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        article_titles, article_contents, article_hrefs, article_images = [], [], [], []

        for tag in soup.findAll("div", {"class": "post-block post-block--image post-block--unread"}):
            tag_header = tag.find("a", {"class": "post-block__title__link"})
            tag_content = tag.find("div", {"class": "post-block__content"})
            tag_image = tag.find("figure", {"class": "post-block__media"})

            article_title = tag_header.get_text().strip()
            article_href = tag_header["href"]
            article_content = tag_content.get_text().strip()
            article_image = tag_image.img['src']

            article_titles.append(article_title)
            article_contents.append(article_content)
            article_hrefs.append(article_href)
            article_images.append(article_image)

        df = pd.DataFrame(
            {"title": article_titles, "content": article_contents, "href": article_hrefs, "image": article_images})
        writer = pd.ExcelWriter(
            'main\\Techcrunch_latest_news.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        self.auto_adjust_excel_columns(writer.sheets['Sheet1'], df)
        writer.save()

        return zip(article_hrefs, article_titles, article_contents)



# GLOBAL APP VARIABLES
app = Flask(__name__)
app.config['SECRET_KEY'] = "9d12c768633d5e7154681084f45d19ed"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# Extentions
db = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)
md = Markdown(app)
gmap = GoogleMaps(app, key="AIzaSyCozLmTJ5vhnHo3kBHG3UXuEHofSm84Xis")

# Importing Routes
from main import routes
