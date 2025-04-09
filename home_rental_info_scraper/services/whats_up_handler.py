from pywa import WhatsApp
from pywa.types import Template as Temp
import os
from dotenv import load_dotenv

load_dotenv()

class WhatsAppHandler(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WhatsAppHandler, cls).__new__(cls)
            # cls.instance.whats_up = WhatsApp()

            cls.instance.whats_up = WhatsApp(
                token=os.environ.get('whats_app_access_token'),
                phone_id=os.environ.get('whats_app_phone_id')
            )
            
            
            return cls.instance
        
    def generate_message(self, sendable_home_list_item: list) -> str:
        message_body = ""
        message_body_list = []
        for sendable_home_item in sendable_home_list_item:
            message_body_list.append(Temp.TextValue(value=sendable_home_item._address))  # {{1}}
            message_body_list.append(Temp.TextValue(value=sendable_home_item.price))  # {{1}}
            message_body_list.append(Temp.TextValue(value=f"€{sendable_home_item.url}\m"))  # {{1}}
            message_body_list.append(Temp.TextValue(value="----------------------------------"))  # {{1}}
            
            
            # message_body += f"Agency name : {sendable_home_item.agency}\n"
            # message_body += f"Address : {sendable_home_item._address}\n"
            # message_body += f"City : {sendable_home_item.city}\n"
            # message_body += f"Price : {sendable_home_item.price}\n"
            # message_body += f"Url : {sendable_home_item.url}\n"
            # message_body += f"-----------------------------------\n\n"
            
        # return message_body
        return message_body_list
    
    """
    This method sends a message to a user on WhatsApp
    @param body: The message to be sent
    @param to: The phone number of the user to send the message to
    @return: True if the message was sent successfully, False otherwise
    """
    def send_message(self, unique_home_list:list, to:str) -> bool:
        if to.startswith('+'):
            to = to[1:]

        for home_item in unique_home_list:
            self.instance.whats_up.send_template(
            
                to = to,
                template=Temp(
                    name='pandjespost',              # Template name
                    language=Temp.Language.DUTCH,       # Dutch language code
                    body=[
                        # Values for the body variables
                        # Temp.TextValue(value='Obrechtstraat 83, Den Haag'),  # {{1}}
                        # Temp.TextValue(value='€3250/m'),                     # {{2}}
                        # Temp.TextValue(value='https://pararius.com/listing/12345'),  # {{3}}
                        Temp.TextValue(value=home_item._address),  # {{1}}
                        Temp.TextValue(value = home_item.price),  # {{2}}
                        Temp.TextValue(value = home_item.url),  # {{3}}
                    ]
                    ,
                    buttons=[                        # Quick reply button
                        Temp.QuickReplyButtonData(data='stop_promotions')  # Payload for "Promoties stoppen"
                    ]
                )
            )