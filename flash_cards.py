#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Handle scraping of Quizlet urls (by chehanr)."""


import re

import requests
from bs4 import BeautifulSoup, SoupStrainer


class FlashCards:
    """Handle scraping.

    :param url: quizlet url.
    :param as_html: Return as html.
    """

    def __init__(self, url, as_html=False):
        self.as_html = as_html
        self.__url = url
        self.__card_dict = {'title': None, 'card': []}

        self.__create_dict()

    def __str__(self):
        _str = '{0} cards at {1}'.format(
            len(self.__card_dict['card']), self.__url)
        return _str

    def __scrape_title(self, header_div):
        title = None

        try:
            heading_tag = header_div.find(
                'h1', attrs={'class': 'UIHeading UIHeading--one'})
            title = heading_tag.text.strip()
        except AttributeError:
            pass
        finally:
            return title

    def __scrape_question(self, card_div):
        question = None

        try:
            question_div = card_div.find(
                'div', attrs={'class': 'SetPageTerm-side'})
            question = question_div

            if not self.as_html:
                question = question_div.text.strip()
        except AttributeError:
            pass
        finally:
            return question

    def __scrape_answer(self, card_div):
        answer = None

        try:
            answer_div = card_div.find(
                'div', attrs={'class': 'SetPageTerm-side'}).findNextSibling('div')
            answer = answer_div

            if not self.as_html:
                answer = answer_div.text.strip()
        except AttributeError:
            pass
        finally:
            return answer

    def __create_dict(self):
        response = requests.get(self.__url, stream=False)
        remote_status_code = response.status_code

        if remote_status_code == requests.codes.ok:
            strainer = SoupStrainer(
                'div', attrs={'class': 'SetPageWrapper-contentContainer'})
            soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
            header_div = soup.find(
                'div', attrs={'class': 'SetPageHeader-container'})
            card_divs = soup.find_all(
                'div', attrs={'class': 'SetPageTerm-content'})

        t = self.__scrape_title(header_div)
        self.__card_dict['title'] = t

        for card_div in card_divs:
            q = self.__scrape_question(card_div)
            a = self.__scrape_answer(card_div)

            card = {'q': q, 'a': a}
            self.__card_dict['card'].append(card)

    def quizlet_id(self):
        id_pattern = r'[^/]\d+[^/]'
        _id = re.findall(id_pattern, self.__url)

        return _id[0]

    def cards(self):
        return self.__card_dict['card']

    def title(self):
        return self.__card_dict['title']
