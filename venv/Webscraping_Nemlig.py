from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re

desired_width = 320
pd.set_option("display.width", desired_width)
pd.set_option("display.max_columns", 30)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

chrome_path = r"C:\Users\Sebas\Desktop\chromedriver_win32 (1)\chromedriver.exe"
###Add all list to a dictionary (final array - wrongly named :)  )
final_array = []

url = ["https://www.nemlig.com/dagligvarer/husholdning/rengoering/opvaskemiddel/opvasketabs-pulver-til-maskine", "https://www.nemlig.com/dagligvarer/husholdning/rengoering/rengoeringsmiddel/luftfrisker"]
for x in url:
    url = x
    browser = webdriver.Chrome(chrome_path, options=chrome_options)
    browser.get(url)

    import time
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    ### Get the descriptions
    all_descriptions = []
    containers = soup.find_all("div", {"class":"productlist-item__info"})
    for container in containers:
        brand = container.text

        all_descriptions.append(brand)

    ### Get the product name
    all_productnames = []
    productnames = soup.find_all("div", {"class":"productlist-item__name"})

    for product in productnames:
        productname = product.text

        all_productnames.append(productname)

    ### Get the base price
    all_basePrices = []
    basePrices = soup.find_all("div", {"class":"pricecontainer__base-price"})
    for price in basePrices:
        x = price.text.strip()
        all_basePrices.append(x)


    ### Get promo price
    all_promoPrices = []
    promoPrices = soup.find_all("div", {"class":"pricecontainer__campaign-price"})
    for promoprice in promoPrices:
        promoprice_ = promoprice.text.strip()
        all_promoPrices.append(promoprice_)


    ### Get Promotexts
    all_promotexts =[]

    for promotext in soup.find_all("div", {"class":"productlist-item__bottom-container"}):
        if promotext.find("span", {"class":"campaign__discount-text-wrap"}):
            x = promotext.find("span", {"class":"campaign__discount-text-wrap"}).text.strip()

            all_promotexts.append(x)

        else:
            all_promotexts.append("")


    ### Get Discount tag
    all_discounttext =[]
    for productlist_item in soup.find_all("productlist-item", {"class":"productlist-show-all__item productlist-item_check-in-basket productlist-item"}):
        try:
            discounttext = productlist_item.find("div", {"class": "campaign__splash-discount"}).text
            all_discounttext.append(discounttext)
        except Exception as e:
            discounttext = ""
            all_discounttext.append(discounttext)

    ### Get Nemlig product number
    all_NemligProductNumber =[]
    for productlist_item in soup.find_all("productlist-item", {"class":"productlist-show-all__item productlist-item_check-in-basket productlist-item"}):
        NemligProductNumber = productlist_item.find("a", {"class":"productlist-item__link"})["ng-href"]
        NemligProductNumber = NemligProductNumber.split("-")[-1]
        all_NemligProductNumber.append(NemligProductNumber)

    ### Get if product sold out
    all_soldOut = []
    for productlist_item in soup.find_all("productlist-item", {"class": "productlist-show-all__item productlist-item_check-in-basket productlist-item"}):
        if productlist_item.find("div", {"class": "productlist-item__soldout"}):
            SoldOut = "SoldOut"
            all_soldOut.append(SoldOut)
        else:
            SoldOut = ""
            all_soldOut.append(SoldOut)

    ### Get brand name
        ### Get the descriptions
        all_brandnames = []
        containers = soup.find_all("div", {"class": "productlist-item__info"})
        for container in containers:
            brandname = container.text.split("/")[-1]

            all_brandnames.append(brandname)



    for Description, Productname, BasePrice, PromoPrice, PromoText, DiscountText, NemligProductNumber, SoldOut, BrandNames in zip(all_descriptions,all_productnames,all_basePrices, all_promoPrices, all_promotexts, all_discounttext, all_NemligProductNumber, all_soldOut, all_brandnames):
        final_array.append({"BrandNames": BrandNames, "Description":Description,"Productname":Productname,"BasePrice":BasePrice, "PromoPrice":PromoPrice, "PromoText":PromoText, "DiscountText":DiscountText, "NemligProductNumber": NemligProductNumber, "SoldOut":SoldOut })

    ###Add final array to dataframe
    df = pd.DataFrame(final_array)

    ### Add Category name to dataframe
    #df["Category"] = url.split("/")[-1]

    ###Add timestamp for each row
    import datetime

    df.insert(0, 'TimeStamp', datetime.date.today())

    ###CLean formatting
    df["BasePrice"] = df["BasePrice"].str.replace(r"\W",".")
    df["PromoPrice"] = df["PromoPrice"].str.replace(r"\W", ".")
    df["PromoPrice"] = df["PromoPrice"].str.replace(r"NaN.0NaN", "")
    df["PromoText"] = df["PromoText"].str.replace(r"\n", "")
    df["PromoText"] = df["PromoText"].str.replace(r"    ", " ")
    df["BasePrice"] = pd.to_numeric(df["BasePrice"])
    df["PromoPrice"] = pd.to_numeric(df["PromoPrice"])
    df["NemligProductNumber"] = pd.to_numeric(df["NemligProductNumber"])



    df.to_excel("output.xlsx", index=False)


    print(df)


###Print Pivot table
#from pivottablejs import pivot_ui
#from IPython.core.display import HTML

#pivot_ui(df,outfile_path="pivottablejs.html")
#HTML("pivottablejs.html")










