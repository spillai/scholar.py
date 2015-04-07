#! /usr/bin/env python
"""
Uses scholar.py to look up urls for each of the bibtex 
entries and updates the howpublished section for each 
of the entries in the bib file. 
"""
# Author: Sudeep Pillai <spillai@csail.mit.edu>                                                                                                                                                          
# License: TODO   

import os.path
import argparse

import bibtexparser
from scholar import ScholarQuerier, ScholarSettings, SearchScholarQuery

def get_url(querier, phrase): 
    # Setup query
    query = SearchScholarQuery()

    # Query title / phrase
    query.set_phrase(phrase)
    
    # Set title search only
    query.set_scope(True)

    # Result count
    query.set_num_page_results(1)

    try: 
        # Send query
        querier.send_query(query)


        articles = querier.articles
        for art in articles:
            url, _, _ = art.attrs['url']
            url_pdf, _, _ = art.attrs['url_pdf']
            return url
    except: 
        return None

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(
        description='biburl.py')
    parser.add_argument(
        '-f', '--bib_file', type=str, required=True,
        help="Bibtex file <references.bib>")
    args = parser.parse_args()


    # Initialize scholar querier
    querier = ScholarQuerier()

    # Setup scholar settings
    settings = ScholarSettings()
    settings.set_citation_format(ScholarSettings.CITFORM_BIBTEX)

    # Apply settings
    querier.apply_settings(settings)

    # Load bib file
    if not os.path.exists(args.bib_file): 
        raise IOException('File does not exist %s' % args.bib_file)

    with open(args.bib_file) as bib_file: 
        bib_db = bibtexparser.load(bib_file)
        for j, item in enumerate(bib_db.entries):
            title = item['title']
            url = get_url(querier, title) 
            if url is not None: 
                item['howpublished'] = '\url{%s}' % url
            print title, url

            if j % 10 == 0: 
                print 'Processed %i out of %i' % (j, len(bib_db.entries))
            
        with open('modified_references.bib', 'w') as modified_bib_file: 
            bibtexparser.dump(bib_db, modified_bib_file)
        

