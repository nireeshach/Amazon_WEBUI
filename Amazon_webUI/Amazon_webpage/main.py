import json
import os
from datetime import datetime
from io import StringIO

import numpy as np
import pandas
import falcon
from falcon_multipart.middleware import MultipartMiddleware
from falcon.http_status import HTTPStatus
from falcon_cors import CORS

from Amazon_Reviews_Scrape.src.scrape_product_reviews import ScrapeReviews
from Amazon_Reviews_Scrape.src.reviews1 import similarity_reviews

public_cors = CORS(allow_all_origins=True)

BASE_DIR = os.getcwd()
STATIC_DIR = os.path.join(BASE_DIR, "static")


class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Methods", "*")
        resp.set_header("Access-Control-Allow-Headers", "*")
        resp.set_header("Access-Control-Max-Age", 1728000)  # 20 days
        if req.method == "OPTIONS":
            raise HTTPStatus(falcon.HTTP_200, body="\n")


class HomePage(object):
    cors = public_cors

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.content_type = "text/html"
        with open("index.html", "r") as f:
            resp.body = f.read()


class GetURL(object):
    cors = public_cors

    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            data = req.stream.read()
            raw_json = json.loads(data)
            url = raw_json["url"]

            df_reviews = ScrapeReviews(url)


            if len(df_reviews.fnl_product_reviews) != 0:
                relevant_reviews_pd, irrelevant_reviews_pd,rating,product_rating = similarity_reviews(
                    df_reviews.fnl_product_reviews
                )

                relevant_results = (
                    relevant_reviews_pd.head(5)
                    .replace(np.nan, "", regex=True)
                    .to_dict("records")
                )

                irrelevant_results = (
                    irrelevant_reviews_pd.head(5)
                    .replace(np.nan, "", regex=True)
                    .to_dict("records")
                )

                status = falcon.HTTP_200
                message = "relevant results"

                resp.status = status
                resp.body = json.dumps(
                    {
                        "message": "resuts loaded sucessfully",
                        "relevant_results": relevant_results,
                        "irrelevant_results": irrelevant_results,
                        "rating":rating,
                        "product_rating": product_rating,
                    }
                )
            else:
                status = falcon.HTTP_500
                message = "Failed get reviews"

                resp.status = status
                resp.body = json.dumps({"message": df_reviews.review_error})

        except:
            status = falcon.HTTP_500
            message = "Failed get reviews"
            resp.status = status
            resp.body = json.dumps({"message": df_reviews.review_error})


# Falcon application object
app = falcon.API(middleware=[MultipartMiddleware(), HandleCORS()])

# Route to serve the resources
app.add_static_route("/static", STATIC_DIR)
app.add_route("/", HomePage())
app.add_route("/getURL", GetURL())
