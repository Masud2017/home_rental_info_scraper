from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from home_rental_info_scraper.spiders import alliantie,antares,atta,bouwinvest,dewoningzoeker,frieslandhuurt,hollandrijnland,hwwonen,ikwilhuren,klikvoorwonen,makelaarshuis,mercatus_aanbod,mosaic_plaza,nmg,noordveluwe,ooms,oostwestwonen,pararius,studentenenschede,svnk,thuisindeachterhoek,thuisinlimburg,thuiskompas,thuispoort,thuispoortstudenten,vbo,vesteda,woninghuren,woninginzicht,wooniezie,woonkeusstedendriehoek,woonnet_rijnmond,woonnethaaglanden,woontij,woonzeker,zuidwestwonen
from home_rental_info_scraper.services.home_services import get_unique_home_list,save_new_homes,send_email_notification_on_user_preferences
import logging



def spider_results():
    try:
        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append(item)
            

        # dispatcher.connect(crawler_results, signal=signals.item_passed)

        process = CrawlerProcess(get_project_settings())
        process.crawl(alliantie.AlliantieSpider)
        process.crawl(antares.AntaresSpider)
        process.crawl(atta.AttaSpider)
        process.crawl(bouwinvest.BouwinvestSpider)
        process.crawl(dewoningzoeker.DewoningzoekerSpider)
        process.crawl(frieslandhuurt.FrieslandhuurtSpider)
        process.crawl(hollandrijnland.HollandrijnlandSpider)
        process.crawl(hwwonen.HwwonenSpider)
        process.crawl(ikwilhuren.IkwilhurenSpider)
        process.crawl(klikvoorwonen.KlikvoorwonenSpider)
        process.crawl(makelaarshuis.MakelaarshuisSpider)
        process.crawl(mercatus_aanbod.MercatusAanbodSpider)
        process.crawl(mosaic_plaza.MosaicPlazaSpider)
        process.crawl(nmg.NmgSpider)
        process.crawl(noordveluwe.NoordveluweSpider)
        process.crawl(ooms.OomsSpider)
        process.crawl(oostwestwonen.OostwestwonenSpider)
        process.crawl(pararius.ParariusSpider)
        process.crawl(studentenenschede.StudentenenschedeSpider)
        process.crawl(svnk.SvnkSpider)
        process.crawl(thuisindeachterhoek.ThuisindeachterhoekSpider)
        process.crawl(thuisinlimburg.ThuisinlimburgSpider)
        process.crawl(thuiskompas.ThuiskompasSpider)
        process.crawl(thuispoort.ThuispoortSpider)
        process.crawl(thuispoortstudenten.ThuispoortstudentenSpider)
        process.crawl(vbo.VboSpider)
        process.crawl(vesteda.VestedaSpider)
        process.crawl(woninghuren.WoninghurenSpider)
        process.crawl(woninginzicht.WoninginzichtSpider)
        process.crawl(wooniezie.WooniezieSpider)
        process.crawl(woonkeusstedendriehoek.WoonkeusstedendriehoekSpider)
        process.crawl(woonnet_rijnmond.WoonnetRijnmondSpider)
        process.crawl(woonnethaaglanden.WoonnethaaglandenSpider)
        process.crawl(woontij.WoontijSpider)
        process.crawl(woonzeker.WoonzekerSpider)
        process.crawl(zuidwestwonen.ZuidwestwonenSpider)
        
        for crawler in process.crawlers:
            crawler.signals.connect(crawler_results, signal = signals.item_passed)
        
        process.start()
        return results
    except Exception as e:
        print(f"Error in spider_results : {e}")
        return None


result = spider_results()
if result is not None:
    print(result)
    print(f"Printing the count of result : {len(result)}")


    home_list = list()
    for item in result:
        home_list.append(item["home"])
        
    logging.info(f"checking the home list :{home_list[0].address}")
    unique_home_list = get_unique_home_list(home_list)
    logging.info(f"printing the size of unique home_list {len(unique_home_list)}")
    if len(unique_home_list) > 0:
        send_email_notification_on_user_preferences(unique_home_list)
        if save_new_homes(unique_home_list=unique_home_list):
            logging.info("New home list added to the database..")
        else:
            logging.info("Something went wrong while trying to save home list to the database")