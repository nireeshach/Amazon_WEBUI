""" Script which gets all product reviews """

import os
import re
import sys
import time
from datetime import datetime
from random import randint
from typing import List
from urllib.parse import urljoin

import pandas

from .common_utils import get_response, CustomeError, write_data

BASEDIR = os.path.dirname(os.path.realpath(__file__))


class ScrapeReviews(object):
    def __init__(
        self,
        product_url: str = None,
        product_urls_file: str = None,
        outfile=None,
        project_dir: str = None,
        pagelimit=None,
        write_data=False,

    ):
        self.time_upper_limit = 120  # Seconds
        self.outfile = outfile
        self.product_url = product_url
        self.product_urls_file = product_urls_file
        self.fnl_product_reviews = []
        self.write_data = write_data
        self.review_error = ""
        if not self.product_url and not self.product_urls_file:
            print("Product Url or Product Urls File should be passed")
            sys.exit()

        if self.product_urls_file and not os.path.isfile(self.product_urls_file):
            print("Given Product Urls File doesn't exist")
            sys.exit()

        self.total_reviews_scraped = 0
        if project_dir:
            self.project_dir = project_dir
        else:
            self.project_dir = BASEDIR

        if not self.outfile:
            self.output_dir = os.path.join(self.project_dir, "output")
            if not os.path.isdir(self.output_dir):
                os.mkdir(self.output_dir)

            self.outfile = os.path.join(self.output_dir, "product_reviews.csv")

        self.pagelimit = pagelimit
        if self.pagelimit:
            self.pagelimit = int(self.pagelimit)

        self.columns = [
            "ProductTitle",
            "ProductDescription",
            "ProductRating",
            "ReviewId",
            "Rating",
            "Title",
            "Date",
            "Verified Purchase",
            "Body",
            "Helpful Votes",
            "ProductUrl",
        ]

        self.get_product_reviews()

    def set_sleep_timer(self):
        # sleep_time = randint(60, self.time_upper_limit)
        sleep_time = randint(5,10)
        print("Sleeping for " + str(sleep_time) + " seconds.\n")
        time.sleep(sleep_time)

    def parse_product_reviews(self, url: str, product_meta={}):
        """ Function which takes review page url as input and
            gets all the reviews

        Args:
            url(str): review page url string
        Returns:
        """
        print("Started process to get product reviews from url: {}".format(url))
        next_page_url = None
        error = None
        product_reviews = []

        resp = get_response(url)

        if resp.get("error"):
            error = resp.get("error")
            self.review_error = error
            return product_reviews, next_page_url, error

        doc = resp["doc"]
        reviews_xpath = '//div[@id="cm_cr-review_list"]//div[@data-hook="review"]'
        for node in doc.xpath(reviews_xpath):
            review_dict = dict(product_meta)

            # Review Id for future reference
            review_dict["ReviewId"] = "".join(node.xpath("./@id"))

            # Rating
            rating_text = "".join(
                node.xpath('.//i[@data-hook="review-star-rating"]/span/text()')
            ).strip()
            if rating_text:
                review_dict["Rating"] = rating_text.split(" ")[0]
            else:
                review_dict["Rating"] = None

            review_dict["Title"] = "".join(
                node.xpath('.//a[@data-hook="review-title"]/text()')
            ).strip()
            review_dict["Date"] = "".join(
                node.xpath('.//span[@data-hook="review-date"]/text()')
            ).strip()

            # Body text
            # to remove <br>, <br/> and </br>
            review_dict["Body"] = (
                "".join(node.xpath('.//span[@data-hook="review-body"]/text()'))
                .replace("<br>", ".")
                .replace("<br/>", ".")
                .replace("</br>", ".")
                .strip()
            )

            # Verified Purchase
            vpurchase_res = node.xpath('.//span[@data-hook="avp-badge"]')
            if vpurchase_res:
                review_dict["Verified Purchase"] = "Yes"
            else:
                review_dict["Verified Purchase"] = "No"

            # Helpful Votes
            vote_text = "".join(
                node.xpath('.//span[@data-hook="helpful-vote-statement"]/text()')
            )
            if vote_text:
                votes = vote_text.split(" ")[0].strip()
                if votes.lower() == "one":
                    votes = "1"
                review_dict["Helpful Votes"] = votes
            else:
                review_dict["Helpful Votes"] = "0"

            product_reviews.append(review_dict)

        next_page_url = "".join(doc.xpath('//li[@class="a-last"]/a/@href')).strip()
        if next_page_url and not next_page_url.startswith("http"):
            next_page_url = urljoin("http://www.amazon.com", next_page_url)

        print("Scraped {} product reviews".format(len(product_reviews)))

        return product_reviews, next_page_url, error

    def get_product_details(self, url: str):
        """ Function which takes prouduct page url as input and
            gets the meta data like Title and Description

        Args:
            url(str): product page url string
        Returns:
        """
        print("Started process to get product meta deta")
        error = None
        product_meta = {}

        resp = get_response(url)
        if resp.get("error"):
            error = resp.get("error")
            self.review_error = error
            return product_meta, error

        doc = resp["doc"]

        # Product Title
        title = "".join(doc.xpath('//span[@id="productTitle"]/text()')).strip()

        # product Description
        desc_xpath = '//div[@id="feature-bullets"]//span[@class="a-list-item"]/text()'
        description = " ".join([i.strip() for i in doc.xpath(desc_xpath) if i.strip()])
        # Removing extra spaces
        description = re.sub(" +", " ", str(description)).strip()

        user_rating_xpath = (
            '//div[@id="averageCustomerReviews_feature_div"]'
            '//span[@class="a-icon-alt"]/text()'
        )
        user_rating_text = "".join(doc.xpath(user_rating_xpath))
        if user_rating_text:
            user_rating = user_rating_text.split(" ")[0]
        else:
            user_rating = None


        review_link_xpath = (
            '//div[@id="reviews-medley-footer"]'
            '//a[@data-hook="see-all-reviews-link-foot"]/@href'
        )
        review_link = "".join(doc.xpath(review_link_xpath)).strip()
        if review_link and not review_link.startswith("http"):
            review_link = urljoin("http://www.amazon.com", review_link)

        product_meta = {
            "ProductTitle": title,
            "ProductDescription": description,
            "reviews_link": review_link,
            "ProductUrl": self.product_url,
            "ProductRating": user_rating,

        }

        return product_meta, error

    def get_product_reviews(self):
        """ Function which takes product url and get reviews """
        start_time = datetime.now()
        print("Started getting reviews for the Product: {}".format(self.product_url))

        # removing outfile if exists
        if os.path.isfile(self.outfile):
            os.remove(self.outfile)

        product_urls = []
        if self.product_urls_file:
            df = pandas.read_csv(self.product_urls_file)
            product_urls.extend(df["product_url"].tolist())

        if self.product_url:
            product_urls.append(self.product_url)

        for product_url in product_urls:
            product_meta, error = self.get_product_details(product_url)
            if error:
                print(error)
                continue

            if not product_meta.get("reviews_link"):
                msg = "Failed to get Reviews link from Product page"
                print(msg)
                continue

            review_url = product_meta.pop("reviews_link")
            pages_scraped = 0
            while True:
                # Calling the same function repeatedly to get product reviews
                # from all the pages until next page url is not found
                # or no reviews are found

                product_reviews, next_page_url, error = self.parse_product_reviews(
                    review_url, product_meta=product_meta
                )
                if error:
                    print(error)

                self.total_reviews_scraped += len(product_reviews)

                if self.write_data:

                    write_data(product_reviews, self.outfile, columns=self.columns)

                else:
                    self.fnl_product_reviews.extend(product_reviews)

  
                if not next_page_url:
                    break

                # As there is nextpage overiding self.url with next_page_url
                review_url = next_page_url
                pages_scraped += 1

                # Sleep because Amazon might block your IP if there are
                # too many requests every second
                self.set_sleep_timer()

                if self.pagelimit and pages_scraped >= self.pagelimit:
                    # To limit the scrape to navigate only particular
                    # pages mentioned by user
                    break

        print(
            "Total Time taken for script to complete: {}, Scraped Reviews: {}".format(
                str(datetime.now() - start_time), self.total_reviews_scraped
            )
        )
        # if self.total_reviews_scraped == 0:
        #     df_reviews = pandas.DataFrame()

        # else:
        #     df_reviews = pandas.Data
        # Frame(self.fnl_product_reviews)
        # return df_reviews

