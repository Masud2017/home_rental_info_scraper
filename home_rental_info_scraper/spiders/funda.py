import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
from twocaptcha import TwoCaptcha
import dotenv
from home_rental_info_scraper.utils.util import parse_city_string
dotenv.load_dotenv()
import os
import requests
import re

solver = TwoCaptcha(os.environ["two_captcha_api_key"])

def get_site_key():
    # res = requests.get(base_url)
    file = open("output.txt", "r")
    data = file.read()
    file.close()
    match = re.search(r'sitekey:\s*["\']([^"\']+)["\']', data)

    site_key:str = ""
    if match:
        site_key = match.group(1)
        print(f"Printing the site key : {site_key}")
    else:
        print("Can not find the sitekey")
    
    return site_key

def solve(base_url,data:str):
    try:
        solved = solver.recaptcha(sitekey=get_site_key(), url=base_url)
        # print(f"Piritnign the caoord : {solved["coordinates"]}")
        return solved.get("code")
        
    except:
        import traceback; traceback.print_exc();
        print(f"Something went wrong while trying to solve the recaptcha. Please have a look at the log.")

def solve_audio(audio_url:str):
    solver = TwoCaptcha(apiKey=os.environ["two_captcha_api_key"])
    # print(f"this is the answer: {solver.audio(file=audio_url, lang="en")}")
    return solver.audio(file=audio_url,lang = "en")

def download_audio(base_url:str):
    print("Attempting downloading the audio file for solving the recaptchav2.")
    req = requests.get(base_url)
    with open("audio_bin.mp3", "wb") as f:
        f.write(req.content)
    if os.path.isfile("audio_bin.mp3"):
        print("Audio file Download complete...")
    else:
        print("File could not be downloaded!!")



def slow_scroll_js():
    return f"""
    async () => {{
        const scrollableDiv = true
        if (scrollableDiv) {{
            var totalHeight = document.body.scrollHeight;
            const step = totalHeight / 10; // Divide the scroll into 10 steps
            let currentPosition = 0;
            
            while (currentPosition < totalHeight) {{
                currentPosition += step;
                window.scrollBy(0, step);
                await new Promise(resolve => setTimeout(resolve, 800));
                if (totalHeight < document.body.scrollHeight) {{
                    totalHeight = document.body.scrollHeight;
                }}
            }}
        }} else {{
            console.error('Scrollable element not found!');
        }}
    }}
    """

class FundaSpider(scrapy.Spider):
    name = "funda"
    allowed_domains = ["www.funda.nl"]
    start_urls = ["https://www.funda.nl/zoeken/huur"]
   
    

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    # PageMethod("wait_for_selector", "button.didomi-components-button", timeout=26000),
                    # PageMethod("click", "//div[contains(@class,'multiple didomi-buttons didomi-popup-notice-buttons')]/button[3]"),
                    
                    # PageMethod("wait_for_selector", 'iframe[src*="recaptcha"]'),
                    # PageMethod("evaluate", """
                    #     async () => {
                    #         const frame = document.querySelector('iframe[src*="recaptcha"]');
                    #         const frameHandle = await window.__playwright_page__.mainFrame().childFrames().find(f => f.url().includes('recaptcha'));
                    #         const checkbox = await frameHandle.waitForSelector('#recaptcha-anchor');
                    #         await checkbox.click();
                    #     }
                    # """)
                ],
            
            },
            headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
        },
            
            
        )
   
   
   
    async def parse(self,response):
        try:
            page_count = 1 # page counter for the pagination logic
            page = response.meta["playwright_page"]
            data = await page.content()
            try:
                element = Selector(text =data).xpath("//h1[contains(@class, 'fd-h1 fd-m-none')]")
                data = await page.content()
                
                with open("output.txt", "w") as f:
                    f.write(data)
                
                if len(element) > 0:
                    print("Shit got the recaptcha.")
                    await page.wait_for_selector('iframe[src*="recaptcha"]', timeout=10000)

                    for frame in page.frames:
                        if "recaptcha" in frame.url:
                            self.logger.info(f"Found reCAPTCHA frame: {frame.url}")
                            checkbox = await frame.query_selector('#recaptcha-anchor')
                            if checkbox:
                                await checkbox.click()
                                self.logger.info("Clicked reCAPTCHA checkbox.")
                            else:
                                self.logger.warning("Checkbox not found in reCAPTCHA frame.")
                            break
                    
                    await page.wait_for_timeout(3000)
                    audio_frame = None
                    for frame in page.frames:
                        if "bframe" in frame.url:
                            audio_button = await frame.query_selector('#recaptcha-audio-button')
                            if audio_button:
                                await audio_button.click()
                                self.logger.info("Clicked audio challenge button.")
                                audio_frame = frame
                            break

                    if not audio_frame:
                        self.logger.warning("Audio challenge frame not found.")
                        return

                    # Step 3: Wait for audio element to load
                    await audio_frame.wait_for_selector('audio', state='attached', timeout=10000)
                    audio_element = await audio_frame.query_selector('audio')

                    if audio_element:
                        audio_src = await audio_element.get_attribute('src')
                        if audio_src:
                            self.logger.info(f"MP3 audio challenge URL: {audio_src}")
                            # yield {"mp3_url": audio_src}
                            download_audio(audio_src)
                            answer = solve_audio(audio_url=os.environ["recaptcha_audio_path"])["code"]
                            input_box = await audio_frame.query_selector('input#audio-response')
                            if input_box:
                                await input_box.fill(answer)
                                self.logger.info("Filled in the answer.")

                                # Click the verify button
                                verify_button = await audio_frame.query_selector('#recaptcha-verify-button')
                                if verify_button:
                                    await verify_button.click()
                                    self.logger.info("Clicked verify button.")
                                else:
                                    self.logger.warning("Verify button not found.")
                            else:
                                self.logger.warning("Input box not found.")
                        else:
                            self.logger.warning("Audio source not found.")
                    else:
                        self.logger.warning("Audio element not found.")
                    
                    await page.wait_for_selector('div.gap-3', timeout=10000)

                    
                    #parsing portion ended
                    
                    try:
                        while True:
                            page = response.meta["playwright_page"]
                            data = await page.content()
                            await page.evaluate(slow_scroll_js())

                            
                            home_card_list = Selector(text=data).xpath("//div[contains(@class, 'flex flex-col gap-3 mt-4')]/div")
                            # parsed_home_list = list()

                            print(f"count of home list : {len(home_card_list)}")
                            for home_card in home_card_list:
                                # await page.wait_for_timeout(3000)
                                url_element = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a")
                                url = ""
                                print(f"Inspecting the url element {url_element}")
                                if len(url_element) > 0:
                                    url = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a").attrib['href']
                                    url = "https://www.funda.nl/" + url
                                    print(f"Debugging the value of url : {url}")
                                else:
                                    url_element = home_card.xpath(".//div/header[contains(@class, 'bg-secondary-10 px-4 py-2')]/following-sibling::*[1]").attrib['href']
                                    url = "https://www.funda.nl/" + url_element
                                    
                                image_element = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a/div/img")
                                image_url = ""
                                if len(image_element) > 0:
                                    image_url = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a/div/img").attrib["srcset"].split(" ")[0]
                                else:
                                    image_alter = home_card.xpath(".//div/header[contains(@class, 'bg-secondary-10 px-4 py-2')]/following-sibling::*[1]/div[1]/div[1]/div[1]/div[2]/img").attrib["srcset"].split(" ")[0]
                                    image_url = image_alter
                                
                                city_element = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[2]/text()")
                                city = ""
                                if len(city_element) > 0:
                                    city = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[2]/text()").get().strip()
                                else:
                                    city_alter = home_card.xpath(".//a[contains(@class, 'text-secondary-70 visited:text-purple-80 hover:text-secondary-70-darken-1 visited:hover:text-purple-80-darken-1 block pr-8')]/div[2]/text()").get().strip()
                                    city = city_alter
                                # debugging purpose only
                                # print(f"debugging the value of city : {home_card.xpath("//a[contains(@class, 'propertyLink')]/figure/figcaption/span[1]").get()}")
                                
                                if city is None:
                                    city = ""
                                address = "" + city
                                # //a[contains(@class, 'text-secondary-70 visited:text-purple-80 hover:text-secondary-70-darken-1 visited:hover:text-purple-80-darken-1 block pr-8')]/div[1]
                                address_element = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[contains(@class,  'flex font-semibold')]/span[1]")
                                address = ""
                                if len(address_element) > 0:
                                    address = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[contains(@class,  'flex font-semibold')]/span[1]/text()").get().strip() + "," + city
                                    city = parse_city_string(city)
                                else:
                                    address_element = home_card.xpath(".//a[contains(@class, 'text-secondary-70 visited:text-purple-80 hover:text-secondary-70-darken-1 visited:hover:text-purple-80-darken-1 block pr-8')]/div[1]/span[1]/text()").get().strip() + "," + city
                                    address = address_element
                                    city = parse_city_string(city)
                                    
                                # import asyncio; await asyncio.sleep(2323232)
                                price = ""
                                if len(home_card.xpath(".//div[contains(@class, 'font-semibold mt-2')]")) > 0:
                                    price = home_card.xpath(".//div[contains(@class, 'font-semibold mt-2')]/div[last()]/text()").get()
                                else:
                                    price = home_card.xpath(".//div[contains(@class, 'font-semibold mt-2')]/div/text()").get()
                                print(f"Inspecting the type of list : {type(price)}")
                                print(f"Now printing the price value ; {price}")
                                if price is not None:
                                    price = price.split(" ")[1]
                                    if "." in price:
                                        price = price.replace(".","")
                                agency = self.name
                                room_count = home_card.xpath(".//div[contains(@class , 'flex space-x-3')]/ul/li[2]/span/text()").get()
                                if room_count is not None:
                                    if "m" in room_count:
                                        room_count = home_card.xpath(".//div[contains(@class , 'flex space-x-3')]/ul/li[3]/span/text()").get()        
                                        
                                    room_count = room_count.split(" ")[0]
                                    if room_count is not None:
                                        room_count = room_count.strip()
                                
                                print("\n--------------------------")
                                print(f"url : {url}")
                                print(f"image_Url = {image_url}")
                                print(f"address : {address}")
                                print(f"city : {city}")
                                print(f"price : {price}")
                                print(f"Name : {agency}")
                                print(f"Room count : {room_count}")
                                print("--------------------------\n")
                                
                            home = Home(
                                address=address,
                                city=city,
                                url=url,
                                agency=agency,
                                price=price,
                                image_url=image_url,
                                room_count=room_count
                            )
                            yield HomeRentalInfoScraperItem(home=home)
                            
                            if page_count > 5:
                                break
                            else:
                                page_count +=1
                            print("Trying to find the next button and scrap the next page.")
                            has_next = response.meta["playwright_page"].locator("//a[contains(@class , 'mx-1 h-8 min-w-8 px-0.5 md:px-2 flex items-center justify-center text-secondary-70 hover:text-secondary-70-darken-1 active:text-secondary-70-darken-2 rounded hover:bg-secondary-10 sm:ml-2 flex items-end md:ml-6')]")
                            if await has_next.is_visible():
                                print("Next pagination button is visible.")
                                await has_next.click()
                             
                                await response.meta["playwright_page"].wait_for_selector("div.gap-3")
                            else:
                                print("Next pagination button is no longer available to quitting.")
                                break
                    except Exception as e:
                        import traceback; traceback.print_exc()
                        # print(f"Error while parsing : {e}")
                        
                    # parsing portion started 
                elif len(element) == 0:
                    print("Didn't got any recaptcha.")    
                    try:
                        while True:
                            page = response.meta["playwright_page"]
                            data = await page.content()
                            await page.evaluate(slow_scroll_js())

                            
                            home_card_list = Selector(text=data).xpath("//div[contains(@class, 'flex flex-col gap-3 mt-4')]/div")
                            # parsed_home_list = list()

                            print(f"count of home list : {len(home_card_list)}")
                            for home_card in home_card_list:
                                # await page.wait_for_timeout(3000)
                                url_element = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a")
                                url = ""
                                print(f"Inspecting the url element {url_element}")
                                if len(url_element) > 0:
                                    url = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a").attrib['href']
                                    url = "https://www.funda.nl/" + url
                                    print(f"Debugging the value of url : {url}")
                                else:
                                    url_element = home_card.xpath(".//div/header[contains(@class, 'bg-secondary-10 px-4 py-2')]/following-sibling::*[1]").attrib['href']
                                    url = "https://www.funda.nl/" + url_element
                                    
                                image_element = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a/div/img")
                                image_url = ""
                                if len(image_element) > 0:
                                    image_url = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a/div/img").attrib["srcset"].split(" ")[0]
                                else:
                                    image_alter = home_card.xpath(".//div/header[contains(@class, 'bg-secondary-10 px-4 py-2')]/following-sibling::*[1]/div[1]/div[1]/div[1]/div[2]/img").attrib["srcset"].split(" ")[0]
                                    image_url = image_alter
                                
                                city_element = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[2]/text()")
                                city = ""
                                if len(city_element) > 0:
                                    city = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[2]/text()").get().strip()
                                else:
                                    city_alter = home_card.xpath(".//a[contains(@class, 'text-secondary-70 visited:text-purple-80 hover:text-secondary-70-darken-1 visited:hover:text-purple-80-darken-1 block pr-8')]/div[2]/text()").get().strip()
                                    city = city_alter
                                # debugging purpose only
                                # print(f"debugging the value of city : {home_card.xpath("//a[contains(@class, 'propertyLink')]/figure/figcaption/span[1]").get()}")
                                
                                if city is None:
                                    city = ""
                                address = "" + city
                                # //a[contains(@class, 'text-secondary-70 visited:text-purple-80 hover:text-secondary-70-darken-1 visited:hover:text-purple-80-darken-1 block pr-8')]/div[1]
                                address_element = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[contains(@class,  'flex font-semibold')]/span[1]")
                                address = ""
                                if len(address_element) > 0:
                                    address = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[contains(@class,  'flex font-semibold')]/span[1]/text()").get().strip() + "," + city
                                    city = parse_city_string(city)
                                else:
                                    address_element = home_card.xpath(".//a[contains(@class, 'text-secondary-70 visited:text-purple-80 hover:text-secondary-70-darken-1 visited:hover:text-purple-80-darken-1 block pr-8')]/div[1]/span[1]/text()").get().strip() + "," + city
                                    address = address_element
                                    city = parse_city_string(city)
                                    
                                # import asyncio; await asyncio.sleep(2323232)
                                price = ""
                                if len(home_card.xpath(".//div[contains(@class, 'font-semibold mt-2')]")) > 0:
                                    price = home_card.xpath(".//div[contains(@class, 'font-semibold mt-2')]/div[last()]/text()").get()
                                else:
                                    price = home_card.xpath(".//div[contains(@class, 'font-semibold mt-2')]/div/text()").get()
                                print(f"Inspecting the type of list : {type(price)}")
                                print(f"Now printing the price value ; {price}")
                                if price is not None:
                                    price = price.split(" ")[1]
                                    if "." in price:
                                        price = price.replace(".","")
                                agency = self.name
                                room_count = home_card.xpath(".//div[contains(@class , 'flex space-x-3')]/ul/li[2]/span/text()").get()
                                if room_count is not None:
                                    if "m" in room_count:
                                        room_count = home_card.xpath(".//div[contains(@class , 'flex space-x-3')]/ul/li[3]/span/text()").get()        
                                        
                                    room_count = room_count.split(" ")[0]
                                    if room_count is not None:
                                        room_count = room_count.strip()
                                
                                if room_count == None:
                                    room_count = "0"
                                if price == None:
                                    price = "0"
                                
                                print("\n--------------------------")
                                print(f"url : {url}")
                                print(f"image_Url = {image_url}")
                                print(f"address : {address}")
                                print(f"city : {city}")
                                print(f"price : {price}")
                                print(f"Name : {agency}")
                                print(f"Room count : {room_count}")
                                print("--------------------------\n")
                                
                            home = Home(
                                address=address,
                                city=city,
                                url=url,
                                agency=agency,
                                price=price,
                                image_url=image_url,
                                room_count=room_count
                            )
                            yield HomeRentalInfoScraperItem(home=home)
                            
                            if page_count > 5:
                                break
                            else:
                                page_count +=1
                            print("Trying to find the next button and scrap the next page.")
                            has_next = response.meta["playwright_page"].locator("//a[contains(@class , 'mx-1 h-8 min-w-8 px-0.5 md:px-2 flex items-center justify-center text-secondary-70 hover:text-secondary-70-darken-1 active:text-secondary-70-darken-2 rounded hover:bg-secondary-10 sm:ml-2 flex items-end md:ml-6')]")
                            if await has_next.is_visible():
                                print("Next pagination button is visible.")
                                await has_next.click()
                            
                                await response.meta["playwright_page"].wait_for_selector("div.gap-3")
                            else:
                                print("Next pagination button is no longer available to quitting.")
                                break
                    except Exception as e:
                        import traceback; traceback.print_exc()
                        # print(f"Error while parsing : {e}")
                    
            except:
                print("Something went while trying to detect the recaptcha. Please have a look at the logs.")
                import traceback; traceback.print_exc()
        except:
            import traceback; traceback.print_exc()
            print("Something went wrong while trying to solve recaptcha.")
            
    # async def parse_data(self, response):
        