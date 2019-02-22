# Amzon Product Reviews Scrape

This project will extract all the reviews for a single product with url passed in command line or multiple products matched the search term passed in command line. This app takes two types of input
* **Search Term**: A search can be passed used command line argument -t or --search-term. When this option is passed the app will search and get all the products from the first two pages of search results and scrape there reviews.
* **Product Url**: Product Url can be directly passed using command line argument -u or --product-url, when this option is passed the app will scrape all the reviews of the particular product.

### **Usage Commands**

```
** Search Tearm **
main.py -t “<search-term>“
Ex: main.py -t “Headophones“

** Product Url **
main.py -u "<url>"
main.py -u "https://www.amazon.com/dp/B00XQCVBAW/
```

### **Input Folder Details**


### **Output Folder Details**
This app generates two outputfiles based on the command line options
* ** Search Term Outfiles **
    * <search_term>_products.csv: CSV file with the product urls that matched the search term, this file used to get the reviews of the matched products
        * Ex: headsets_products.csv
    * <search_term>_product_reviews.csv: CSV with the Reviews of all the matched products
        * Ex: headsets_product_reviews.csv
    * Note: These files will be overided if we run the app with -t or --search-term option with same search term as the previous run.

* ** Product Url Outfile **
    * product_reviews.csv: CSV with all the reviews of the product url which was passed in command line.
    * Note: This file will be overided evertime we run the app with -u or --product-url option.
        
### **Installation Notes**
Requirements needed for this project 
lxml==4.3.0
requests==2.21.0
pandas==0.23.4 

### **Known Issues/Problems**
