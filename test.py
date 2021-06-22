import bs4
import requests


class ScrapeNews():
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



        return zip(article_hrefs, article_titles, article_contents, article_images)


    def return_news(self):
        scraped_data = self.scrape()
        news = [i for i in scraped_data]
        
        return news

