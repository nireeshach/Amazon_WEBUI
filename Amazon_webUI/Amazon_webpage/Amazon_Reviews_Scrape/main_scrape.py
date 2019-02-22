"""Script to Scrape Reviews of all the Products mathcing a search tearm"""

import argparse
import os
import sys

from src.scrape_reviews import AmazonReviews
from src.scrape_product_reviews import ScrapeReviews

PROJECTDIR = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--search-term",
        dest="search_term",
        help="SearchTerm for matching the products",
    )
    parser.add_argument(
        "-r",
        "--product-pages",
        dest="product_pages",
        default=2,
        type=int,
        help="Max number of pages for to get matched products",
    )

    parser.add_argument(
        "-u", "--product-url", dest="product_url", help="Product URL to scrape reviews"
    )

    parser.add_argument(
        "-p",
        "--page-limit",
        dest="page_limit",
        default=None,
        type=int,
        help="Max number of pages for to product reviews, scrapes all pages by default",
    )

    args = parser.parse_args()

    if not args.search_term and not args.product_url:
        print("Either Search Term or Product Url should be passed to scrape reviews")
        sys.exit()

    if args.search_term:
        # If search term argument is passed we will call AmazonReviews class
        AmazonReviews(
            args.search_term,
            product_page_limit=args.product_pages,
            review_page_limit=args.page_limit,
            project_dir=PROJECTDIR,
        )
    else:
        # If product url is passed we will call ScrapeReviews class
        ScrapeReviews(
            args.product_url, pagelimit=args.page_limit, project_dir=PROJECTDIR
        )
