
import lxml.html
from pupa.scrape import Scraper, Person
from lxml import etree
import json
import inflection
import pprint

class GUPersonScraper(Scraper):
  

    def scrape(self, chamber=None, session=None):
        if session is None:
            session = self.latest_session()
            self.info('no session specified, using %s', session)
        
        yield self.scrape_upper(session)


    def scrape_upper(self, session):
        ordinal = inflection.ordinalize(session)
        web_url = 'http://www.guamlegislature.com/senators_{}.htm'.format(ordinal)
        page = lxml.html.fromstring(self.get(url=web_url).content)
        member_rows = page.xpath('//center//td[contains(@class,"just")]')
        for row in member_rows:
            if row.xpath('.//span[contains(@class,"picturename")]/text()'):
                member_name = row.xpath('.//span[contains(@class,"picturename")]/text()')[0].strip()
                member_name = member_name.replace('Honorable ','')
                member_email = row.xpath('.//a[contains(@href,"mailto")]/@href')[0].strip()

                member_title = 'member'
                if row.xpath('.//strong[contains(@class,"title")]/text()'):
                    member_title = row.xpath('.//strong[contains(@class,"title")]/text()')[0]
            
                all_text = row.xpath('descendant-or-self::*/text()')

                member_phone = ''
                member_fax = ''
                for subrow in all_text:
                    if 'ph.' in subrow.lower():
                        member_phone = subrow.strip().replace('Ph.:','')
                    if 'fax:' in subrow.lower():
                        member_fax = subrow.strip().replace('Fax.:','')
                    if 'committee on' in subrow.lower():
                        pass
                        #print ("Committee: ")
                        #print (subrow.strip().replace('Commitee on',''))

                person = Person(name=member_name,
                                role=member_title,
                                primary_org="Legislature of Guam")

                if member_phone:
                    person.add_contact_detail(type='voice', value=member_phone)
                if member_fax:
                    person.add_contact_detail(type='fax', value=member_fax)
                if member_email:
                    person.add_contact_detail(type='fax', value=member_email)
                
                person.add_source(url=web_url)
                yield person