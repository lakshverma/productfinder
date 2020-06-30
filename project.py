"""
New Product Finder v0.1

Written by Lakshay Verma.

New Product Finder features:
1. Get the H&M t shirts web page using Requests
2. Extract/Parse useful info: Name of the product, price, link to the product.
3. Check for any new products (by comparing it with product list from the last time when script was run)
4. Print a list of new products with useful info

FAQs:

Q1. Why am I getting the message 'Whoops! There is no new data.'?
A. Since you were testing the script by removing rows of data from base_products.csv, after the script is done running
once, the new_products.csv is renamed as base_products.csv so that the latest data can be used as a base when the script
is run next time. If you run the script again within a short span of time, data in base_products.csv will technically be
the same as data in new_products.csv as no new products have been added. Therefore, the update.csv file will be empty
and print an empty data frame with just the file headers.

Q2. Why are you exporting the data in csv files instead of storing it using dictionaries?
A. Because I wanted to learn how to manipulate csv files with python. Also, eventually I was planning to write the
script in a way that it automatically emails you a csv file with new products (update.csv). Better suggestions are
always welcome!

Upcoming features:

1. Ability to email the new products list
2. Add support for other countries. The program currently only supports the India website
3. Ability to look up different types of products in different categories
4. A fancy GUI so that people don't have to rely on the terminal to use the program

"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

print(r'''


 _   _                ______              _            _    ______ _           _                     _____       __  
| \ | |               | ___ \            | |          | |   |  ___(_)         | |                   |  _  |     /  | 
|  \| | _____      __ | |_/ / __ ___   __| |_   _  ___| |_  | |_   _ _ __   __| | ___ _ __  __   __ | |/' |     `| | 
| . ` |/ _ \ \ /\ / / |  __/ '__/ _ \ / _` | | | |/ __| __| |  _| | | '_ \ / _` |/ _ \ '__| \ \ / / |  /| |      | | 
| |\  |  __/\ V  V /  | |  | | | (_) | (_| | |_| | (__| |_  | |   | | | | | (_| |  __/ |     \ V /  \ |_/ /  _  _| |_
\_| \_/\___| \_/\_/   \_|  |_|  \___/ \__,_|\__,_|\___|\__| \_|   |_|_| |_|\__,_|\___|_|      \_/    \___/  (_) \___/
                                                                                                                                                                                                                                      

Note: the program currently only supports check new products under Men's t-shirts category from the H&M website and 
performs that operation by default. The program needs the following packages/libraries to perform its task correctly:
1. OS
2. Requests
3. Beautiful Soup
4. Pandas

''')

URL = 'https://www2.hm.com/en_in/men/shop-by-product/tshirts-tank-tops.html'
HM_URL_PREFIX = 'https://www2.hm.com'

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}


def scrape_hm_products(filename):
    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find the element that contains info about total number of products in this product category
    load_products = soup.find_all('h2', class_='load-more-heading')

    # Loop over the object to extract the total number of products listed in this product category
    for num_products in load_products:
        total_products = num_products['data-total']

    # Recreate the url by combining the original URL with the necessary link parameters and total number of products
    # Adding the total number of products in the page-size parameter displays all products at once
    scrape_url = URL + '?product-type=men_tshirtstanks&sort=stock&image-size=small&image=model&offset=0&page-size=' + \
                 total_products

    # Since we want to actually want to scrape data from scrape_url, reassigning new values to page and soup
    page = requests.get(scrape_url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Grab each product
    product_elems = soup.find_all('li', class_='product-item')

    # Create/Overwrite a new csv file to store scraped data
    # filename = 'products.csv'
    f = open(filename, 'w')

    # Set the csv file headers
    headers = 'Product Name, Price, Link\n'
    f.write(headers)

    # Loop over every index item
    for product_elem in product_elems:
        product_name = product_elem.div.next_sibling.h3.a.string
        product_price = product_elem.div.next_sibling.strong.span.string
        product_link = HM_URL_PREFIX + product_elem.div.a['href']

        # print('product name: ' + product_name)
        # print('product price: ' + product_price)
        # print('product link: ' + product_link)
        # print(end='\n' * 3)

        # Write all looped over values to the csv file
        f.write(product_name + ',' + product_price.replace(',', '') + ',' + product_link + "\n")

    f.close()


def main():
    # check if the program has been run before. If yes, the base file 'base_products.csv' exists. In this case,
    # the program will create a new csv file (new_products.csv) that will used to compare and check if new products
    # are added. Any new rows of data will be written to update.csv which is then printed to the console.
    if os.path.exists('base_products.csv'):
        scrape_hm_products('new_products.csv')
        # Open both CSVs to compare and check if new products have been added since the last time this script was run
        with open('base_products.csv', 'r') as t1, open('new_products.csv', 'r') as t2:
            fileone = t1.readlines()
            filetwo = t2.readlines()

        with open('update.csv', 'w') as outFile:
            # Write headers to the new csv file (update.csv) that eventually prints new products to console
            headers = 'Product Name, Price, Link\n'
            outFile.write(headers)
            # Write all new products to update.csv
            for line in filetwo:
                if line not in fileone:
                    outFile.write(line)
        # Print update.csv to console to show new products in a pretty manner.
        df = pd.read_csv('update.csv')

        if df.empty:
            print('Whoops! There are no new products. Check again later. Want to know why are you seeing this message? '
                  'Check out Question 1 in the FAQs section of the first comment in the source code.')
        else:
            with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
                print(df)

        # After comparision is done, rename the new file as the base file so that comparision can be done next time
        # the script is run. Added WindowsError as exception since Windows doesn't let you overwrite without deleting
        # original files.
        try:
            os.rename('new_products.csv', 'base_products.csv')
        except WindowsError:
            os.remove('base_products.csv')
            os.rename('new_products.csv', 'base_products.csv')

    # If there is no base_products.csv file, program will create one and tell the user that they need to run the
    # script again in a few days to see new products. Alternatively, base file can be modified for testing the script.
    else:
        scrape_hm_products('base_products.csv')
        print('Thanks for running this script! Since this is your first time, there are no new products to show. Run '
              'script again in a couple of days to check out new products.')
        print('Alternatively, you can delete 3-4 of rows '
              'from the end of base_products.csv file right now and run the script again just to see how this script '
              'works.')


if __name__ == '__main__':
    main()
