# quizlet2pdf

A simple script to save quizlet flashcards as PDFs.

## Usage

Run `python quizlet2pdf.py`

### Additional Options

    usage: quizlet2pdf [-h] [-u URLS] [-f FILE] [-d DEST]

    Save quizlet flashcards as PDFs (by chehanr).

    optional arguments:
    -h, --help            show this help message and exit
    -u URLS, --urls URLS  quizlet urls (comma separated)
    -f FILE, --file FILE  quizlet urls txt file
    -d DEST, --destination DEST
                            dir to save PDFs

### Prerequisites

- Run `pip install -r "requirements.txt"`
- Install [wkhtmltopdf](https://wkhtmltopdf.org/) and add it to `PATH`.