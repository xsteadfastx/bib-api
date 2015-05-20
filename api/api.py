# -*- coding: utf-8 -*-
from bottle import route, request, run
from marshmallow import Schema, fields
from api import browser


class SearchResultSchema(Schema):
    '''The schema for the search results items.
    Needed for the serialization.'''
    name = fields.String()
    available = fields.Boolean()
    year = fields.Date()
    type = fields.String()


class SearchPostSchema(Schema):
    search = fields.String(required=True)


@route('/api/search', method='POST')
def search():
    data = SearchPostSchema().load(request.json)

    if data.errors:
        return dict(error=data.errors)

    results = browser.search(data.data['search'])

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


@route('/api/rented', method='POST')
def rented():
    data = RentPostSchema().load(request.json)

    if data.errors:
        return dict(errors=data.errors)

    rent_list = browser.rent_list(data.data['cardnumber'],
                                  data.data['password'])

    schema = RentResultSchema(many=True)
    results = schema.dump(rent_list)

    return dict(results=results.data)
