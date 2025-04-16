import logging
import requests
import json
from home_rental_info_scraper.models.Home import Home
from ..config.db_handler import query_db
from .secrets import MAIL_GUN_API,MAIL_GUN_API_URL,MAIL_GUN_FROM_EMAIL_ADDRESS
import traceback
import jsonpickle




class EmailHandler:
    def __init__(self):
        self.MAILGUN_API_URL = MAIL_GUN_API_URL
        self.FROM_EMAIL_ADDRESS = MAIL_GUN_FROM_EMAIL_ADDRESS
    
    def generate_email_message(self, homes):
        home_cards = "".join(f'''
            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="margin-bottom: 20px; border: 1px solid #ddd; border-radius: 4px; max-width: 600px;">
            
                <tr>
                    <td style="padding: 10px; vertical-align: top;">
                        <img src="{home.image_url}" alt="Home Image" style="display: block; width: 100px; height: 100px; border-radius: 4px; margin-right: 10px;" />
                    </td>
                    <td style="padding: 10px; vertical-align: top;">
                        <p style="margin: 0; font-size: 14px; line-height: 1.5;"><strong>Address:</strong> {home.address}, {home.city}</p>
                        <p style="margin: 0; font-size: 14px; line-height: 1.5;"><strong>Price:</strong> €{home.price}/m</p>
                        <p style="margin-top: 10px;">
                            <a href="{home.url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: #ff9800; color: #ffffff; padding: 8px 16px; text-decoration: none; font-size: 14px; border-radius: 4px;">View</a>
                        </p>
                    </td>
                </tr>
            </table>
        ''' for home in homes)

        html_template = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Home List</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; margin: 0;">
            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color: #ffffff; max-width: 600px; margin: 0 auto; border-collapse: collapse;">
                <tr>
                    <td style="padding: 20px; text-align: center; background-color: #ff9800; color: #ffffff;">
                        <h1 style="font-size: 24px; margin: 0;">Your Home List <strong>Alert</strong></h1>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 20px; text-align: center;">
                        <p style="font-size: 16px; margin: 0;">{len(homes)} new matches for you.</p>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 0;">
                        {home_cards}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 20px; text-align: center; background-color: #f4f4f4;">
                        <p style="font-size: 12px; color: #888;">This is an automated email. Please do not reply.</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        '''
        
        with open("test.html", "w") as file:
            file.write(html_template)
        return html_template


    
    def send_single_email(self, to_address: str, subject: str, message: str, home_list : list = {}, home_count:int = 0):
        try:
            api_key = MAIL_GUN_API
            resp = requests.post(
                self.MAILGUN_API_URL,
                auth=("api", api_key),
                data={
                    "from": self.FROM_EMAIL_ADDRESS,
                    "to":to_address,
                    "subject": subject,
                    "text": message,
                    # "html": message,
                    "template": "home rental info notification",
                    "h:X-Mailgun-Variables": jsonpickle.encode({"home_list": home_list, "home_count":str(home_count),"fav_icon": "https://iili.io/3lxGVGj.jpg"}, unpicklable=False),
                    # "v:home_count": home_count,
                    # "v:home_list_json_resource" : requests.get(new_db_url).json()
                    # "X-Mailgun-Template-Variables": '{"test": "test"}'
                }
            )
            if resp.status_code == 200:
                logging.info(f"Successfully sent an email to '{to_address}' via Mailgun API.")
            else:
                logging.error(f"Could not send the email, reason: {resp.text}")
        except Exception as ex:
            logging.exception(f"Mailgun error: {ex}")
            traceback.print_exc()

# if __name__ == "__main__":
#     email_handler = EmailHandler()
    
#     # home = hestia.Home()
#     home = Home()
#     home.address = "1234 Main St"
#     home.city = "New York"
#     home.price = 1000
#     home.agency = "Agency"
#     home.url = "https://facebook.com"
    
#     homes = [home]
#     message = email_handler.generate_email_message(homes)
#     email_handler.send_single_email("msmasud578@gmail.com", "New Homes", message)
