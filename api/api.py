# -*- coding: utf-8 -*-
from bottle import Bottle, request, response, abort
from marshmallow import Schema, fields
from itsdangerous import URLSafeSerializer, BadSignature
from urllib.parse import urljoin
from os import environ
from sys import exit
import datetime
import redis

from api import browser, ical


# check for some environment variables
if 'SECRET_KEY' not in environ:
    exit('no SECRET_KEY environment variable set')
else:
    SECRET_KEY = environ['SECRET_KEY']

if 'REDIS_HOST' not in environ:
    exit('no REDIS_HOST environment variable set')
else:
    REDIS_HOST = environ['REDIS_HOST']

# define app
app = Bottle()

DOCUMENTATION_INTRO = '''
<h1>Unofficial Stadtbibliothek Nürnberg API</h1>
<p>For rolling your own API or help developing it,
check <a href="https://github.com/xsteadfastx/bib-api">GitHub</a>.</p>
'''


@app.route('/')
def index():
    '''The documentation page.
    '''
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
    Needed for the serialization.
    '''
    name = fields.String()
    available = fields.Boolean()
    year = fields.Date()
    type = fields.String()


class SearchPostSchema(Schema):
    name = fields.String(required=True)


@app.route('/api/search', method='POST')
def search():
    '''Returns searched items.
    <br>Example: `http POST /api/search name='python'`
    '''
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


class AuthSchema(Schema):
    cardnumber = fields.String(required=True)
    password = fields.String(required=True)


@app.route('/api/rented', method='POST')
def rented():
    '''Returns rented items.
    <br>Example: `http POST /api/rented cardnumber='B12345' password='pass'`
    '''
    data = AuthSchema().load(request.json)

    if data.errors:
        return dict(errors=data.errors)

    rent_list = browser.rent_list(data.data['cardnumber'],
                                  data.data['password'])

    schema = RentResultSchema(many=True)
    results = schema.dump(rent_list)

    return dict(results=results.data)


@app.route('/api/ical-url', method='POST')
def get_ical_url():
    '''Returns url for using ical calendar with rented items and return dates.
    <br>Example: `http POST /api/ical-url cardnumber='B12345' password='pass'`
    '''
    data = AuthSchema().load(request.json)

    if data.errors:
        return dict(errors=data.errors)

    s = URLSafeSerializer(SECRET_KEY)

    base = '{}://{}'.format(request.urlparts.scheme, request.urlparts.netloc)

    url = urljoin(base, 'ical/rented.ics?token={}'.format(s.dumps(data)))

    return dict(url=url)


@app.route('/ical/rented.ics', method='GET')
def rented_ical():
    '''Returns a ical file with all return dates for the rented items.
    Needs a token argument. Use the '/api/ical-url' endpoint for getting the
    full url.
    '''
    if 'token' not in request.query.dict.keys():
        return dict(errors='no token')

    try:
        # set response header type
        response.set_header('Content-type', 'text/calendar')

        # get token from request query
        token = request.query.dict['token'][0]

        # check token. throws a exception if something is wrong with the token
        s = URLSafeSerializer(SECRET_KEY)
        data = s.loads(token)[0]

        # check if there is a redis entry for the token
        r = redis.StrictRedis(host=REDIS_HOST)

        redis_entry = r.hgetall(token)
        if redis_entry:
            two_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(
                hours=2)
            updated = datetime.datetime.strptime(
                redis_entry[b'updated'].decode('utf-8'),
                '%Y-%m-%d %H:%M:%S.%f')

            if updated > two_hours_ago:
                return redis_entry[b'ical'].decode('utf-8')

        ical_file = ical.build_ical(data['cardnumber'], data['password'])

        # store ical_file in redis
        r.hmset(token, dict(ical=ical_file,
                            updated=datetime.datetime.utcnow()))

        return ical_file

    except BadSignature:
        abort(401)

    except:
        abort(500)
