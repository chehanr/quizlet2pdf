#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A simple script to save quizlet flashcards as PDFs (by chehanr)."""

import os
from argparse import ArgumentParser
from random import randint

import pdfkit

from flash_cards import FlashCards


def main(urls, dest=None):
    """Main work."""

    css = 'base.css'

    if not dest:
        dest = 'pdfs/'

    if not os.path.exists(dest):
        os.makedirs(dest)

    for i, url in enumerate(urls):
        print('\nurl {0}/{1} ({2})'.format(i+1, len(urls), url))

        fc = FlashCards(url, as_html=True)
        q_id = fc.quizlet_id()
        title = fc.title()
        flashcards = fc.cards()

        html = ''
        html += '<h1><a href="{0}">{1}</a></h1>'.format(url, title)

        for i, flashcard in enumerate(flashcards):
            q = flashcard['q']
            a = flashcard['a']

            line = '<div class="card">{0}<br>{1}</div>'.format(q, a)
            html += line
            html += '<br>'

        if not q_id:
            q_id = randint(0, 9999)

        pdfkit.from_string(
            html, '{0}/{1}-{2}.pdf'.format(dest, title, q_id), css=css)


def arg_parse():
    """Argument parser."""

    parser = ArgumentParser(prog='quizlet2pdf',
                            description='save quizlet flashcards as PDFs (by chehanr).')
    parser.add_argument('-u', '--urls', action='store', dest='urls',
                        help='quizlet urls (comma separated)', required=False)
    parser.add_argument('-f', '--file', action='store', dest='file',
                        help='quizlet urls txt file', required=False)
    parser.add_argument('-d', '--destination', action='store', dest='dest',
                        help='dir to save PDFs', required=False)
    results = parser.parse_args()

    return results


if __name__ == '__main__':
    args = arg_parse()
    urls = []

    if not args.urls and not args.file:
        print('\nurls not entered, type -h for help.')
    elif args.file:
        with open(args.file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not line.startswith('#'):
                    urls.append(line.strip())
    elif args.urls:
        urls = [(item) for item in args.urls.split(',')]

    main(urls, args.dest)
