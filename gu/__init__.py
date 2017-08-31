# coding: utf-8
from pupa.scrape import Organization
from pupa.scrape import Jurisdiction

from datetime import datetime

from .people import GUPersonScraper
from .bills import GUBillScraper

#from .utils import get_all_pages

class GU(Jurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:us/territory:gu'
    division_name = 'Guam'
    name = 'Legislature of Guam'
    url = 'http://www.guamlegislature.com/'
    parties = [
        {'name': 'Democratic Party'},
        {'name': 'Republican Party'},
    ]
    scrapers = {
        "people": GUPersonScraper,
        "bills": GUBillScraper,
    }

    # http://lda.data.parliament.uk/sessions.json
    legislative_sessions = [
        {"identifier":"32",
         "name":"32nd Session",
         "start_date": "2017-01-01"},
        {"identifier":"33",
         "name":"33rd Session",
         "start_date": "2017-01-01"},
        {"identifier":"34",
         "name":"34th Session",
         "start_date": "2017-01-01"},
    ]


    def get_organizations(self):
        legislature = Organization(name="Legislature of Guam",
                                   classification="legislature")        
        yield legislature

        upper = Organization('Guam Senate', classification='upper', parent_id=legislature)

        yield upper