import json
import re

import bs4
import requests

from bundestag import BtPage

__all__ = ['BtPage']


def main():
    master_url = ('https://www.bundestag.de/ajax/filterlist/de'
                  '/mediathek/536668-536668?documenttype=44235'
                  '4%23BTFaisSpeechRecord&limit=70&mediaCategor'
                  'y=442350%23Plenarsitzungen&noFilterSet=false&'
                  'offset={}&rednerIds=442354%239399%20OR%20750%20'
                  'OR%206861%20OR%206862%20OR%206598%20OR%203097%2'
                  '0OR%203096%20OR%208360')
    ccc = 0
    for i in range(0, 500, 70):
        url = master_url.format(i)

        r = requests.get(url)

        if r.status_code != 200:
            raise ValueError('Unable to fetch page {}: {}'.format(url, r.status_code))

        links_ids = re.findall(r'mediathek\?videoid=(\d+)', r.text)

        for id_ in links_ids:
            rr = requests.get(f'https://www.bundestag.de/mediathekoverlay?videoid={id_}&view=main&videoid={id_}')
            if rr.status_code != 200:
                raise ValueError('Unable to fetch page {}: {}'.format(url, rr.status_code))

            data = bs4.BeautifulSoup(rr.text, 'html.parser').find('span', class_='bt-dachzeile')

            l = re.findall(r'/dokumente/textarchiv[^"]+', rr.text)
            print(ccc := ccc + 1, data.get_text(strip=True), l)
            if not l:
                continue

            for link in l:
                p = BtPage('https://www.bundestag.de' + link)
                p.date = data.get_text(strip=True)
                with open(f'pages/bt/{id_}.json', 'w', encoding='utf-8') as f:
                    json.dump(p.get_data().model_dump(), f, indent=4, ensure_ascii=False)

                with open('pages/bt.txt', 'a', encoding='utf-8') as f:
                    f.write(str(p.plain_text) + '\n')


if __name__ == '__main__':
    main()
