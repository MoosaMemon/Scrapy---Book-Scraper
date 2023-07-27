import scrapy
import datetime
from bookscraper.items import BookItem
import random

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    # this parse functions get called when the response comes back
    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            relative_url = book.css("h3 a::attr(href)").get()

            if("catalogue/" in relative_url):
                book_url = f"https://books.toscrape.com/{relative_url}"
            else:
                book_url = f"https://books.toscrape.com/catalogue/{relative_url}"
            # callback is the function that will get executed once comes back from the url that we go into
            yield response.follow(book_url, callback=self.parse_book_page)  
            
        

        next_page = response.css("li.next a::attr(href)").get()
        if(next_page is not None):
            if("catalogue/" in next_page):
                next_page_url = f"https://books.toscrape.com/{next_page}"
            else:
                next_page_url = f"https://books.toscrape.com/catalogue/{next_page}"
            # callback is the function that will get executed once comes back from the url that we go into
            yield response.follow(next_page_url, callback=self.parse)
        
    def parse_book_page(self, response):
        product = response.css("article.product_page")
        table_rows = product.css("table tr")
        book_item = BookItem()

        book_item["title"] = product.css(".row .product_main h1::text").get()
        book_item["url_of_prod"] = response.url
        book_item["product_description"] = product.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item["product_category"] = product.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item["upc"] = table_rows[0].css("td::text").get()
        book_item["product_type"] = table_rows[1].css("td::text").get()
        book_item["rating"] = product.css("p.star-rating").attrib['class']
        book_item["tax"] = table_rows[4].css("td::text").get()
        book_item["price_without_tax"] = table_rows[2].css("td::text").get()
        book_item["price_with_tax"] = table_rows[3].css("td::text").get()
        book_item["number_of_reviews"] = table_rows[6].css("td::text").get()
        availability = table_rows[5].css("td::text").get().split(" ")[0:2]
        if(availability[0] == "In"):
            book_item["InStock"] = True 
        book_item["num_of_items_available"] = table_rows[5].css("td::text").get().split(" ")[-2].split("(")[-1]
        book_item["current_price"] = product.css(".row .product_main p.price_color::text").get()
        book_item["date"] = datetime.datetime.now(tz=datetime.timezone.utc)

        yield book_item




