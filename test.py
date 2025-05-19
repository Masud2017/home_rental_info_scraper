import requests
import re
from twocaptcha import TwoCaptcha
import dotenv
import os
dotenv.load_dotenv()
def get_site_key(base_url):
    res = requests.get(base_url)
    with open("output_.txt", "w") as f:
        f.write(res.text)
        
    file = open("output.txt", "r")
    data = file.read()
    file.close()
    match = re.search(r'sitekey:\s*["\']([^"\']+)["\']', data)

    site_key:str = ""
    if match:
        site_key = match.group(1)
        print(f"Printing the site key : {site_key}")
    return site_key


def solve_aduio(audio_url:str):
    solver = TwoCaptcha(apiKey=os.environ["two_captcha_api_key"])
    print(f"this is the answer: {solver.audio(file=audio_url, lang="en")}")
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
if __name__ == "__main__":
    print(f"The site kye is : {get_site_key("https://www.funda.nl/zoeken/huur")}")
    # https://www.google.com/recaptcha/api2/payload/audio.mp3?p=06AFcWeA60rTrB5bOa7tvjKfKWVMr-o_h7PVn7RmQokTTh6ljMQEtXSBttS3d77Ln0d_tgtoVial58AbnINTwmC7yPIvV0pWGBzW8cb553g-NrKLiQgUG5fPctWp7BTxwEYkhepDAQlazlakEGMmX4dktfGcNSedXpCsnrwskwUETJ1Ty_iLIClodTZpMyZEHrrh6cNwbNOKtu&k=6LdVe6UZAAAAAJkilxwQAziiaj02gsg9ben_hSAa
    download_audio("https://www.google.com/recaptcha/api2/payload/audio.mp3?p=06AFcWeA6Pt6pBKWFiq7ZcYW6FY4abhgwwZzYdfmqox92C6XkfVlkqSRD6jrhJxlj4tnejEv7yw1zy3Dv4t9ZYquDrDWxC7vqejO3yQItIHA0L-j5LWq2KNK5YeJwPO_sh8vH0IQ4HCBXq3oPCueeoP1PGFFw_yHrkHW5pChz2fK43dY8UbgVPxzrrj8jZp4PXLpOaM4Ta8o66&k=6LdVe6UZAAAAAJkilxwQAziiaj02gsg9ben_hSAa")
    print(f"So this is the audio response: {solve_aduio("https://www.funda.nl/zoeken/huur", "bin.mp3")}")
    
    
    
    