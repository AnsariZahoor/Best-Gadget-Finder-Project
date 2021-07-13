
# Best Gadget Finder

End-to-End Data Science group project conduct by Packt & TeamEpic.

## Problem Statement:
Best Gadget Finder, a new startup to help users compare products at a single platform. It requires to pull data from various e-commerce websites and then compare product names across e-commerce websites. And then having a UI to search gadgets and see a detailed comparative UI.


## Technology stack

| Element   | Description   | 
| :-------- | :------- |
| **Python** | Programming language |
| **BeautifulSoup** |  Python library used for web scraping  |
| **Selenium** | Used to automate web application |
| **Pandas** |  Python library used for data manipulation & analysis |
| **Elasticsearch** | Full-text search and analytics engine |
| **Kibana** | Used for visualizing Elasticsearch data |
| **Requests** | Python library used for making HTTP requests |
| **Postman** | API client helps to build, test and modify APIs |
| **Flask** |  Used for making web applications and creating API |
| **HTML CSS** | Basic language for website designing |
| **Bootstrap** | CSS framework used to create interative website |


## Process Flow

**1. Web Scraping** : We scraped the mobile products data from Amazon, Flipkart and Snapdeal by 
using Python programming language.

**2. Data cleaning** : Data cleaning is the process of fixing or removing incorrect, corrupted, incorrectly formatted, 
duplicate, or incomplete data within a dataset.

**3. Data Standardization** : We have created a new column of unique ID for each product with the help of for loop. Customer may search a product name 
in different styles. Like phone brand with its color, phone brand with its storage. Our system 
should be able to provide the results by identifying these keywords

**4. Name matching** : As we had three different source files with the same product but with different way of naming 
the products. We used FuzzyWuzzy python library to match two strings and get a score form 
the FuzzyWuzzy Library.

**5. Data Mapping** : We needed to collect all the data from three different files match the names and aggregate 
the data in one record for all three different sources. All the products are mapped based on 
their name from all three sources.

**6. Elastic Search** : We created an instance of the Elasticsearch and indexed the filed 
in elastic search. Once the data was present, we created a query to get the matching result 
from the database.

**7. API development** : Created an API using Flask. We fetched data from elastic search with accurate result.

**8. Data testing** : After getting such results we have test these result and we get 97% accuracy.

**9. UI Development** : UI created using HTML,CSS & Bootstrap.

**10. Deployment** : Backend created using flask web framework. In backend we have used flask 
API which is used for managing http requests. Here we used fetch API function to get the data from elastic search. 
And used this data to display the result in frontend.

As a final 
result we can see a website with three sources Amazon Flipkart and Snapdeal. Also, there is 
a button provided like buy now, by clicking on it user will automatically get redirected to the 
product link and can buy the desired product


https://user-images.githubusercontent.com/66164268/124423829-9084ab00-dd83-11eb-9409-1ee77d6e507f.mp4

