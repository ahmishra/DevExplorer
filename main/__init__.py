"""
Heart of the app :)

PYLINT: 9.80/10
"""


# Other Imports / Extentions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext.markdown import Markdown
from flask_mail import Mail

# Tech Crunch Scraper

import bs4
import requests


class ScrapeNews():

    """
    Class that will be used in routes.py to get the scraped news info
    """

    def scrape(self):

        """
        :params: none

        Main news scraper
        """

        response = requests.get("https://techcrunch.com/")

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        article_titles, article_contents, article_hrefs, article_images = [], [], [], []

        for tag in soup.findAll("div",{"class": "post-block post-block--image post-block--unread"}):

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

        return zip(article_hrefs, article_titles, article_contents, article_images)


    def return_news(self):

        """
        :params:none

        Returns the news in parseable format
        """

        scraped_data = self.scrape()
        news = []

        for a_news in scraped_data:
            news.append(a_news)

        return news




# Main App
app = Flask(__name__)


# Extentions
db = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)
md = Markdown(app)
news_scraper = ScrapeNews()
mail = Mail(app=app)
login_manager = LoginManager(app)


# GLOBAL APP VARIABLES
app.config['SECRET_KEY'] = "9d12c768633d5e7154681084f45d19ed"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 0000
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'devexplorerh1@gmail.com'
app.config['MAIL_PASSWORD'] = "explorer11thousand"
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Importing Routes (AT THE END TO AVOID CIRCULAR IMPORTS)
from main import routes
