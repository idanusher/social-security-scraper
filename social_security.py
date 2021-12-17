import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

hp = r'https://www.btl.gov.il/mediniyut/situation/statistics/BtlStatistics.aspx?type=2&id=9'
exp = r'BtlStatistics.aspx?type=1&amp;id=\d{1,}'
regex = re.compile(exp)

class SocialSecurity:
    def __init__(self):
        '''
        initializing make a pandas df named self.cities_df, to hold each city name, code , and social security web link.
        '''
        html = requests.get(hp)
        soup = BeautifulSoup(html.content, 'html.parser')
        ths = soup.find_all('th')
        table_rows = []
        for i in ths:
            i = str(i)
            i = BeautifulSoup(i, "html.parser")
            ais = i.find('a')
            if ais:
                city_string = str(ais)
                bs = BeautifulSoup(city_string, 'html.parser').find('a')
                city_name = bs.getText()
                city_link = bs['href']
                city_code = int(city_link.split("=")[-1])
                row_for_table = dict(city_name=city_name, city_link=city_link, city_code=city_code)
                table_rows.append(row_for_table)
        self.cities_df = pd.DataFrame(table_rows)
        pass


    def get_cities_attribute(self, attributes):
        exp = 'th_MISPAR_MKABLIM8,th1,th1a'
        begil_exp = r'th_MVGR,th1,th1a'
        skirim_exp = 'th_SCHIRIM,th1,th1a'
        mize_exp = r'th_SCHIRIM_VAZMAIM,th1,th1a'
        selfers_exp = r'th_AZMAIM,th1,th1a'

        cities_urls = [f"https://www.btl.gov.il/mediniyut/situation/statistics/{end}" for end in list(self.cities_df['city_link'])]
        rows = []
        for u in cities_urls:
            new_row = dict()
            new_row['city_id'] = u.split("=")[-1]

            url_page = BeautifulSoup(requests.get(u).content, 'html.parser')
            sal = url_page.find(id=exp).getText()
            begil=url_page.find(id=begil_exp).getText()
            skirim=url_page.find(id=skirim_exp).getText()
            mize=url_page.find(id=mize_exp).getText()
            selfers=url_page.find(id=selfers_exp).getText()

            new_row.update(dict( sal=sal, begil=begil, skirim=skirim, mize=mize, sefers=selfers))
            rows.append(new_row)

        result_df = pd.DataFrame(data=rows)
        result_df.to_csv('results.csv', index=False)
        print("done")


ss = SocialSecurity()
ss.get_cities_attribute()