"""Script to Scrape Reviews of all the Products mathcing a search tearm"""

import os
import sys
import argparse
import pdb
from datetime import datetime

from .common_utils import CustomeError
from .scrape_product_urls import ScrapeProducts
from .scrape_product_reviews import ScrapeReviews

BASEDIR = os.path.dirname(os.path.realpath(__file__))


class AmazonReviews(object):
    def __init__(
        self,
        search_term: str,
        product_page_limit=None,
        review_page_limit=None,
        project_dir: str = None,
    ):
        """
        Calling main function directly from initialization method

        Args:
            search_term(str): SearchTerm for matching the products
            project_dir(str): Project directory full path
        """
        self.reviews_scraped = 0
        self.product_asins = set()
        self.search_url = "http://www.amazon.com/s/ref=nb_sb_noss/?field-keywords={}"
        self.product_page_limit = product_page_limit
        self.review_page_limit = review_page_limit
        self.search_tearm = search_term
        if not self.search_tearm:
            msg = "Search term can't be empty/None"
            print(msg)
            raise CustomeError(msg)

        if project_dir:
            self.project_dir = project_dir
        else:
            self.project_dir = BASEDIR

        self.output_dir = os.path.join(self.project_dir, "output")
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        self.main()

    def main(self):
        """
        Main function which takes the searchterm and 
        searches for the matching products and there reviews
        """
        start_time = datetime.now()

        print("Started Scraping Products")
        stime = datetime.now()
        # Getting ASIN ids of products matching the search term
        search_url = self.search_url.format(self.search_tearm)
        formatted_search_term = self.search_tearm.replace(" ", "_").lower().strip()
        products_outfile = os.path.join(
            self.output_dir, "{}_products.csv".format(formatted_search_term)
        )
        ScrapeProducts(search_url, products_outfile, pagelimit=self.product_page_limit)
        print(
            "Time taken to get products asins: {}".format(str(datetime.now() - stime))
        )

        # Scraping reviews of each product ASIN parsed above
        review_outfile = os.path.join(
            self.output_dir, "{}_product_reviews.csv".format(formatted_search_term)
        )
        ScrapeReviews(
            product_urls_file=products_outfile,
            outfile=review_outfile,
            pagelimit=self.review_page_limit,
        )

        print(
            "Total Time taken for script to complete: {}, Scraped Reviews: {}".format(
                str(datetime.now() - start_time), self.reviews_scraped
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--search-term",
        dest="search_tearm",
        required=True,
        help="SearchTerm for matching the products",
    )

    parser.add_argument(
        "-p",
        "--product-pages",
        dest="product_pages",
        default=10,
        type=int,
        help="Max number of pages for to get matched products",
    )

    parser.add_argument(
        "-r",
        "--review-pages",
        dest="review_pages",
        default=None,
        type=int,
        help="Max number of pages for to product reviews",
    )

    args = parser.parse_args()
    AmazonReviews(
        args.search_term,
        product_page_limit=args.product_pages,
        review_page_limit=args.review_pages,
    )
