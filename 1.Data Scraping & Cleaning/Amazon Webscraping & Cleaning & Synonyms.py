from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

s = HTMLSession()

#list to collect all the data
productList = []
searchterm = 'mobile'
Amazon_id = []
synonyms = []

#url with all the brands of mobiles are selected
url = f'https://www.amazon.in/s?k={searchterm}&i=electronics&rh=n%3A1389432031%2Cp_89%3AASUS%7CAlcatel%7CApple%7CBlackBerry%7CGionee%7CGoogle%7CHTC%7CHonor%7CHuawei%7CIKALL%7CIntex%7CLG%7CLava%7CLenovo%7CMI%7CMicromax%7CMicrosoft%7CMoto%7CMotorola%7CNokia%7COnePlus%7COppo%7CPanasonic%7CRedmi%7CSHIVANSH%7CSamsung%7CSnexian%7CTecno%7CVivo%7CXiaomi%7CXifo%7Citel%7Crealme&dc&qid=1623924901&rnid=3837712031&ref=sr_pg_1'
urltest = 'https://www.amazon.in/s?k=mobile&ref=nb_sb_noss'

# Functions get data from url and saves it in  soup(beautifulsoup) variable which it returns for us to work with
def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup


def nameSplitter(name_string):
    for i in range(0, len(name_string)):
        x = name_string[i].split(' ', 1)
        Bname = x[0]
        rest = x[1]
        if Bname == '(Renewed)':
            w = rest.split(' ', 1)
            Pname = w[0]
            rest = w[1]
            attrval = rest[rest.find("(") + 1:rest.find(")")]
            attrval = attrval.split(',')
            try:
                Namelist = [Pname + attrval[0], Pname + attrval[1]]

            except:
                Namelist = [Pname + attrval[0]]


            synonyms.append(Namelist)
            print(Namelist)
            print('w')

        elif bool(re.search('\(', rest)):
            y = rest.split('(', 1)
            modelno = y[0]
            if Bname=='New':
                Pname =  modelno
            else:
                Pname = Bname + ' ' + modelno

            attrval = rest[rest.find("(") + 1:rest.find(")")]
            attrval = attrval.split(',')

            try:
                Namelist = [Pname, Pname + attrval[0], Pname + attrval[1]]

            except:
                Namelist = [Pname, Pname + ' ' + attrval[0]]

            synonyms.append(Namelist)
            print(Namelist)
            print('y')

        elif bool(re.search('\|', rest)):
            v = rest.split('\|')
            Pname = v[0]

            try:
                Namelist = [Bname, Pname, Pname + v[1]]

            except:
                Namelist = [Bname, Pname]

            synonyms.append(Namelist)
            print(Namelist)
            print('v')

        elif bool(re.search(',', rest)):
            z = rest.split(',')

            try:
                Namelist = [Bname + ' ' + z[0], Bname + z[0] + ' ' + z[1], Bname + z[0] + z[2]]
            except:
                Namelist = [Bname + ' ' + z[0], Bname + z[0] + z[1]]

            synonyms.append(Namelist)
            print(Namelist)
            print('z')
        else:
            Namelist = []
            Namelist.append(Bname + ' ' + rest)
            synonyms.append(Namelist)


#Function to extract data from the soup object and get the desired results stored in the dictionary which is then stored in the list
def getproducts(soup):
    # Extracting all the divs which are of the type s-search result as the contain the result there is no differentiating with sponsored products but they are of the same category
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    for item in products:

        try:
            #Extracting the product name from the item that contains the product name
            Productname = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).get_text()
       # print(Productname)
        except:
            # Extracting the product name from the item that contains the product name in case text attribute does not exist
            Productname = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})

        try:
            # Extracting the sales price from the item that contains the price
            salesPrice = item.find('span', {'class': 'a-price-whole'}).get_text()

        except:
            # Extracting the sales price from the item that contains the price in case text attribute is missing or no value is present
            salesPrice = item.find('span', {'class': 'a-price-whole'})
            #  print(salesPrice)
            #If value for sales price does not exists update to Unavailable
            if str(salesPrice) == 'None':
                salesPrice='Unavailable'
     #   print(salesPrice)

        try:
            # Extracting the original price from the item that contains the price
            oldPrice = item.find('span', {'class': 'a-price a-text-price'}).find('span', {'class': 'a-offscreen'}).get_text()
            oldPrice = str(oldPrice).replace('₹', '')
        except:
            # Extracting the sales price from the item that contains the price when text attribute is not present
            oldPrice = item.find('span', {'class': 'a-offscreen'})
            # For instance where we get the are not able to get the string but still we have the entire element we match it to extract the price value from the element
            if str(oldPrice)[0:12] == '<span class=':
                pattern = '>(.*?)<'
                oldPrice=re.search(pattern, str(oldPrice)).group(1)
                oldPrice=str(oldPrice).replace('₹', '')
            # if value does not exist replace with Unavailable
            if str(oldPrice) == 'None':
                oldPrice='Unavailable'


      #  print(oldPrice)

        try:
            # Extracting the Ratings data from the item that contains the value
            reviewvalue = item.find('span', {'class': 'a-icon-alt'}).get_text()
            # If value for Ratings does not exist replace with NA
            if str(reviewvalue) == 'None':
                reviewvalue = 'NA'
            # If value exist format as per requirments
            else:
                reviewvalue = str(reviewvalue)[0:3]
        except:
            # If Ratings does not have text attribute
            reviewvalue = item.find('span', {'class': 'a-icon-alt'})
            # update the value to NA
            if str(reviewvalue) == 'None':
                reviewvalue = 'NA'
      #  print(reviewvalue)

        # Get the element that has the link
        Link = item.find('a', {'class': 'a-link-normal a-text-normal'})

        #get the actual link after adding the missing part of the url
        productlink ='https://www.amazon.co.in' + str(Link['href'])
        #print(productlink)

        #get the item with the image
        image = item.find('img', {'class': 's-image'})
        #Extract the imagelink
        imagelink=image['src']
        #print(imagelink)

        #Check and add availability column
        if str(salesPrice)=='Unavailable':
            availability='Unavailable'
        else:
            availability = 'Available'

        # Remove coma from sales price and old price
        commavalue = ','
        if commavalue in str(salesPrice):
            salesPrice = str(salesPrice).replace(',', '')

        if commavalue in str(oldPrice):
            oldPrice = str(oldPrice).replace(',', '')



        #Create a dictionary to update all the value for one product
        Productdetails = {
            'Name': Productname,
            'SalesPrice': salesPrice,
            'OriginalPrice': oldPrice,
            'Availability':availability,
            'Ratings': reviewvalue,
            'ProductLink': productlink,
            'ImageLink': imagelink
        }
        #Add the dictionary to list
        productList.append(Productdetails)
    return
# Function to check if at the end of the page does the next button exist or not
def getnextpage(soup):
    #get the elements of the page number buttons
    pages = soup.find('ul', {'class': 'a-pagination'})
    #Find if the page has the value of the last page if not then update the url value
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url ='https://www.amazon.co.in' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    #when we reach the last page functions return nothing which we check against the while loop to exit the loop
    else:
        return
'''
testing
soup = getdata(url)
getproducts(soup)
df = pd.DataFrame(productList)
print(productList)
'''


def mainfunc(url):
    urlvale=url
    while True:
        soup = getdata(url)
        getproducts(soup)
        url = getnextpage(soup)
        if not url:
            break
        else:
            print(url)
    return



def loaddata(list):
    df = pd.DataFrame(list)
    df_clean = df.drop_duplicates(subset=['Name'], keep='first')
    for i in range(1, len(df_clean) + 1):
        idVal = f'Amazon_{i}'
        Amazon_id.append(idVal)

    df_clean.insert(0, 'Id', Amazon_id, True)

    namelist = df_clean['Name'].tolist()
    nameSplitter(namelist)

    df_clean.insert(2, 'Synonyms', synonyms, True)



    # df_clean = df_clean.sort_values (['Name'], ascending=1)

    df_clean.to_csv('AmazonProductdata.csv', index=False)
    return


mainfunc(url)
loaddata(productList)



'''
#Runs all the function as per the login and updates the product list
while True:
    soup = getdata(url)
    getproducts(soup)
    url = getnextpage(soup)
    if not url:
        break
    else:
        print(url)
#add the productlist to a pandas dataframe and export to csv
df = pd.DataFrame(productList)
df_clean = df.drop_duplicates(subset=['Name'], keep='first')
df_clean.to_csv('Productdata.csv', index=False)
'''