""" Script which gets all product urls matching the search term """

import os
import time
from random import randint
from typing import List
from urllib.parse import urljoin

import lxml

from .common_utils import get_response, CustomeError, write_data


class ScrapeProducts(object):
    def __init__(self, url, outfile, pagelimit=None):
        self.time_upper_limit = 120  # Seconds
        self.url = url
        self.outfile = outfile
        self.pagelimit = pagelimit
        if self.pagelimit:
            self.pagelimit = int(self.pagelimit)

        self.get_products_data()

    def set_sleep_timer(self):
        # sleep_time = randint(60, self.time_upper_limit)
        sleep_time = 10
        print("Sleeping for " + str(sleep_time) + " seconds.\n")
        time.sleep(sleep_time)

    def get_product_urls(self, url: str):
        """ Function which takes search url as input and
            gets all the product urls
        
        Args:
            url(str): search url string
        Returns:
        """
        print("Started process to get products from url: {}".format(url))
        next_page_url = None
        error = None
        product_urls = []

        resp = get_response(url)
        if resp.get("error"):
            error = resp.get("error")
            return product_urls, next_page_url, error

        doc = resp["doc"]
        # Xpath to get all the products urls matched the search term
        product_urls_xpath = (
            '//ul[contains(@class, "s-result-list")]'
            '//li[@data-asin and not(contains(@class, "container-background")) '
            'and not(.//p[contains(text(), "Shop by Category")])]'
            '//a[contains(@class, "s-access-detail-page")]/@href'
        )

        for url in doc.xpath(product_urls_xpath):
            if not url:
                continue
            if not url.startswith("http"):
                url = urljoin("http://www.amazon.com", url)
            product_urls.append(url)

        if not product_urls:
            # product_xpath might failed or no results found
            error = "Products xpath failed or no results found, returned empty list"
            return product_urls, next_page_url, error

        next_page_url = "".join(doc.xpath('//a[@id="pagnNextLink"]/@href')).strip()
        if next_page_url and not next_page_url.startswith("http"):
            next_page_url = urljoin("http://www.amazon.com", next_page_url)

        print("Scraped {} products from page: {}\n".format(len(product_urls), url))

        return product_urls, next_page_url, error

    def get_products_data(self):
        """ Function which takes search url as input and parses results """

        print("Started getting product urls")
        # removing outfile if exists
        if os.path.isfile(self.outfile):
            os.remove(self.outfile)

        pages_scraped = 0
        while True:
            # Calling the same function repeatedly to get product urls
            # from all the pages until next page url is not found
            # or no results are found
            product_urls, next_page_url, error = self.get_product_urls(self.url)
            if error:
                raise CustomeError(error)

            write_data(product_urls, self.outfile, columns=["product_url"])
            import pdb

            pdb.set_trace()

            if not next_page_url:
                break

            # As there is nextpage overiding self.url with next_page_url
            self.url = next_page_url
            pages_scraped += 1

            # Sleep because Amazon might block your IP if there are too many requests every second
            self.set_sleep_timer()

            if self.pagelimit and pages_scraped >= self.pagelimit:
                # To limit the scrape to navigate only particular
                # pages mentioned by user
                break
