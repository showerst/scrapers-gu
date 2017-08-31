import lxml.html
from pupa.scrape import Scraper, Bill, VoteEvent
from lxml import etree
from datetime import datetime
import inflection
import pytz
#from .utils import get_all_pages
import pprint

# http://lda.data.parliament.uk/meta/bills/_id.json
# http://lda.data.parliament.uk/bills.json?session.displayName=2016-2017&_view=description&_pageSize=10&_page=0&originatingLegislature.prefLabel=House%20of%20Lords

class GUBillScraper(Scraper):
    tz = pytz.timezone('Europe/London')

    def scrape(self,session=None,chamber=None):
        if not session:
            session = self.latest_session()
            self.info('no session specified, using %s', session)

        yield from self.scrape_upper(session)

    def scrape_upper(self, session):
        ordinal = inflection.ordinalize(session)
        web_url = 'http://www.guamlegislature.com/{}_bills_intro_content.htm'.format(ordinal)
        content = self.get(url=web_url).text
        sections = content.split('<!--Start of bill-->')
        for section in sections[1:-1]:
            if section.strip():
                print ("\n")
                print (section)
                fragment = lxml.html.fromstring(section)

                # Some <a><strong>'s are missing their open strong tag.
                if fragment.xpath('//a/strong/text()'):
                    bill_title = fragment.xpath('//a/strong/text()')[0].strip()
                else:
                    bill_title = fragment.xpath('//a[1]/text()')[0].strip()
                print(bill_title)

                question = fragment.xpath('*/text()')[0].strip()
                print(question)
        # page = lxml.html.fromstring(self.get(url=web_url).content)
        # # $ns1[count(.|$ns2) = count($ns2)]
        # bill_rows = page.xpath('*[count(.|preceding::comment()[contains(.,"Start of bill")]) = count(following::comment()[contains(.,"end of bill")])]')
        # for row in bill_rows:
        #     all_text = row.xpath('descendant-or-self::*/text()')
        #     print(all_text)
        #     print("\n\n")
        # bill = Bill(identifier=page['identifier']['_value'],
        #             legislative_session=session,
        #             title=page['label']['_value'],
        #             classification='bill')        

        # bill.add_sponsorship(name=str(sponsor['sponsorPrinted']), 
        #                     classification="Primary",
        #                     entity_type="person",
        #                     primary=True)

        # bill.add_version_link(note=version['label']['_value'],
        #             url=version['homePage'],
        #             date=version['date']['_value'],
        #             media_type=version['contentType'],
        #             on_duplicate='ignore')
        # bill.add_document_link(note=version['label']['_value'],
        #                     url=version['homePage'],
        #                     date=version['date']['_value'],
        #                     media_type=version['contentType'],
        #                     on_duplicate='ignore
        # act = bill.add_action(description=action['billStageType']['title'],
        #                 chamber=chamber,
        #                 date=action['billStageSittings'][0]['date']['_value'],
        #                 classification=action_class, #see note about allowed classifications
        #                 )

