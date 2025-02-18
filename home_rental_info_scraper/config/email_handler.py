import logging
import requests
import re
from home_rental_info_scraper.models.Home import Home
from ..config.db_handler import query_db



class EmailHandler:
    def __init__(self):
        self.MAILGUN_API_URL = "https://api.mailgun.net/v3/sandbox9663794f3e4d4009a9dde37a6db4dc45.mailgun.org/messages"
        self.FROM_EMAIL_ADDRESS = "Mailgun Sandbox <postmaster@sandbox9663794f3e4d4009a9dde37a6db4dc45.mailgun.org>"
    
    def generate_email_message(self, homes):
        home_cards = "".join(f'''
            <div class="card_container">
                <img src="https://via.placeholder.com/150" alt="Home Image">
                <div class="card-right_side">
                    <ul>
                        <li><strong>Address:</strong> {home.address}, {home.city}</li>
                        <li><strong>Price:</strong> €{home.price}/m</li>
                    </ul>
                    <a href="{home.url}" target="_blank">View</a>
                </div>
            </div>
        ''' for home in homes)

        html_template = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Home List</title>
            <style>
                * {{ margin: 0; padding: 0; }}
                .card_container{{ width: 25rem; padding: .5rem; border-radius: .4rem; border: 1px solid black; display: flex; flex-direction: row; gap: 2rem; }}
                .card_container img {{ width: 8rem; height: 8rem; }}
                .container {{ padding: 1rem; }}
                .card-grp {{ margin-top: 1.5rem; display: flex; flex-direction: column; gap: .5rem; align-items: center; }}
                .card-right_side{{ display: flex; flex-direction: row; gap: .5rem; width: 100%; }}
                .card-right_side ul {{ list-style-type: none; flex-grow: 10; display: flex; flex-direction: column; justify-content: center; }}
                .card-right_side a {{ background: orange; color: white; border-radius: .5rem; width: 5rem; height: 2rem; display: flex; justify-content: center; align-items: center; text-decoration: none; }}
                .card-right_side a:hover {{ background: #cc8400; transition: .2s background-color; }}
            </style>
        </head>
        <body class='container'>
            <div style="text-align: center;">
                <h1>Your Home List <strong>Alert</strong></h1>
                <span>{len(homes)} new matches for you.</span>
            </div>
            <div class="card-grp">
                {home_cards}
            </div>
        </body>
        </html>
        '''
        return html_template
    
    def send_single_email(self, to_address: str, subject: str, message: str):
        try:
            api_key = ""
            resp = requests.post(
                self.MAILGUN_API_URL,
                auth=("api", api_key),
                data={
                    "from": self.FROM_EMAIL_ADDRESS,
                    "to": to_address,
                    "subject": subject,
                    "text": message,
                    "html": message
                }
            )
            if resp.status_code == 200:
                logging.info(f"Successfully sent an email to '{to_address}' via Mailgun API.")
            else:
                logging.error(f"Could not send the email, reason: {resp.text}")
        except Exception as ex:
            logging.exception(f"Mailgun error: {ex}")

if __name__ == "__main__":
    email_handler = EmailHandler()
    
    # home = hestia.Home()
    home = Home()
    home.address = "1234 Main St"
    home.city = "New York"
    home.price = 1000
    home.agency = "Agency"
    home.url = "https://facebook.com"
    
    homes = [home]
    message = email_handler.generate_email_message(homes)
    email_handler.send_single_email("Masud <msmasud578@gmail.com>", "New Homes", message)
