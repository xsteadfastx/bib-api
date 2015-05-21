# -*- coding: utf-8 -*-
from bottle import Bottle, request
from marshmallow import Schema, fields
from api import browser

app = Bottle()

DOCUMENTATION_INTRO = '''
<h1>Stadtbibliothek Nürnberg API</h1>
<p>For rolling your own API or help developing it,
check <a href="https://github.com/xsteadfastx/bib-api">GitHub</a>.</p>
'''


@app.route('/')
def index():
    '''The documentation page.'''
    documentation = DOCUMENTATION_INTRO
    documentation += '<table id="api-endpoints"><tbody>\n'
    documentation += ('<tr>'
                      '<th style="text-align: left">Endpoint</th>'
                      '<th style="text-align: left">Method</th>'
                      '<th style="text-align: left">Description</th>\n')
    for route in app.routes:
        documentation += (
            '\n<tr><td>' + route.rule + '</td><td>' + route.method +
            '</td><td>' + str(route.callback.__doc__) + '</td></tr>')
    documentation += '</tbody></table>'

    return documentation


class SearchResultSchema(Schema):
    '''The schema for the search results items.
    Needed for the serialization.'''
    name = fields.String()
    available = fields.Boolean()
    year = fields.Date()
    type = fields.String()


class SearchPostSchema(Schema):
    name = fields.String(required=True)


@app.route('/api/search', method='POST')
def search():
    '''Returns searched items.
    Example: `http POST /api/search name='python'`'''
    data = SearchPostSchema().load(request.json)

    if data.errors:
        return dict(error=data.errors)

    results = browser.search(data.data['name'])

    # serialize the data
    schema = SearchResultSchema(many=True)
    result = schema.dump(results)

    # bottle converts the dict to holy json
    return dict(results=result.data)


class RentResultSchema(Schema):
    name = fields.String()
    from_date = fields.Date()
    till_date = fields.Date()
    notes = fields.String()


class RentPostSchema(Schema):
    cardnumber = fields.String(required=True)
    password = fields.String(required=True)


@app.route('/api/rented', method='POST')
def rented():
    '''Returns rented items.
    Example: `http POST /api/rented cardnumber='B12345' password='pass'`'''
    data = RentPostSchema().load(request.json)

    if data.errors:
        return dict(errors=data.errors)

    rent_list = browser.rent_list(data.data['cardnumber'],
                                  data.data['password'])

    schema = RentResultSchema(many=True)
    results = schema.dump(rent_list)

    return dict(results=results.data)
