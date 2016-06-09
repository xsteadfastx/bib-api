from flask import current_app, jsonify, request, Response, g
from itsdangerous import URLSafeSerializer
import arrow

from app.mod_api import mod_api, schemes
from app.mod_api.decorators import valid_facility, valid_token
from app.mod_api.errors import InvalidUsage
from app.mod_api.ical import build_ical


@mod_api.route('/facilities', methods=['GET'])
def facility_list():
    """List all available facilities.

    Request::

        http GET "localhost:5000/api/facilities"

    Response::

        {
            "facilities": [
                "wolfsburg"
            ]

        }
    """
    return jsonify(facilities=list(current_app.facilities.keys()))


@mod_api.route('/<facility>/search', methods=['POST'])
@valid_facility
def search(facility):
    """Search library for items.

    It takes a JSON-object in a POST request. You also can put a
    request argument with the name "page" to the url for pagnation.
    Most times the library search forms return more items then they fit on a
    single page. So they need some kind of pagination. If the page argument
    is given, it will search for the page number and browse to that page
    before parsing the result. If not given, it will use the page number "1".
    Here is a example:

    Request::

        http POST "localhost:5000/api/wolfsburg/search?page=4" term="batman"

    Response::

        {
            "next_page": 5,
            "results": [
                {
                    "annotation": "Der Schurke Two-Face wurde durch...",
                    "author": "geschrieben von Matthew K. Manning.",
                    "copies": [
                        {
                            "available": false,
                            "branch": "01:Kinderbibl. Zentr",
                            "due_date": "2016-02-05",
                            "id": "M1400963",
                            "position": "4.1 Mann",
                            "type": "Kinder- und Jugendliteratur"
                        }
                    ],
                    "cover": "http://foo.bar/images/P/3555829.03.MZZZZZZZ.jpg",
                    "isbn": "978-3-596-85582-7",
                    "title": "Batman - Ein finsterer Plan",
                    "year": "2013-01-01"
                }
            ]
        }


    :param facility: The facility to search in.
    :type facility: str
    """
    # get term and validate it
    json_data, errors = schemes.SearchRequest().load(request.get_json())

    if errors:
        raise InvalidUsage(errors)

    # parse request args for page
    if request.args.get('page'):
        if not request.args.get('page').isdigit():
            raise InvalidUsage('page type not integer')

        page = int(request.args.get('page'))
    else:
        page = 1

    # perform search and marshmallow it
    results = current_app.facilities[facility]['search'](json_data['term'],
                                                         page)
    data = schemes.SearchResponse().dump(results)

    return jsonify(data.data)


@mod_api.route('/<facility>/token', methods=['POST'])
@valid_facility
def get_token(facility):
    """Creates a authentication token.

    This endpoint returns a authentication token for a specific facility.

    Request::

        http POST localhost:5000/api/wolfsburg/token username=foo password=bar

    Response::

        {
            "token": "eyJwYXNzd29yZCI6IjoiZm9vIn0.DmRMyew4ukCAZHsnIrs4PaY8"

        }

    :param facility: The facility to get a token for.
    :type facility: str
    """
    post_data = request.get_json()

    # if there is no data raise an error
    if not post_data:
        raise InvalidUsage('no data')

    # get authentication data and validate it
    json_data, errors = schemes.TokenRequest().load(post_data)

    if errors:
        raise InvalidUsage(errors)

    # create serializer
    s = URLSafeSerializer(current_app.config['SECRET_KEY'], salt=facility)

    # create token
    token = s.dumps(json_data)

    # scheme it
    data = schemes.TokenResponse().dump({'token': token})

    return jsonify(data.data)


@mod_api.route('/<facility>/lent', methods=['GET'])
@valid_facility
@valid_token
def lent_list(facility):
    """Returns a list of lent items and the saldo of the account.

    This view returns all lent items in a list with the title and author
    plus the date until the item needs to get returned. It also tries to get
    the saldo of the account.

    Request::

        http GET localhost:5000/api/wolfsburg/lent?token=pIUBfh1BSvoROF8wgHse

    Response::

        {
            'saldo': '-36,00',
            'items': [
                {
                    'due_date': '2016-04-15', 'author': 'Dürer, Albrecht',
                    'title': 'Albrecht Dürer'
                }, {
                    'due_date': '2016-04-15', 'author': 'Hopkins, John',
                    'title': 'Modezeichnen'
                }, {
                    'due_date': '2016-04-15', 'author': 'Hopper, Edward',
                    'title': 'Edward Hopper'
                }
            ]
        }

    :param facility: The facility to get a lent list from.
    :type facility: str

    """
    s = URLSafeSerializer(current_app.config['SECRET_KEY'], salt=facility)

    token = request.args['token']

    userdata = s.loads(token)

    lent_list = current_app.facilities[facility]['lent_list'](
        userdata['username'], userdata['password'])

    data = schemes.LentListResponse().dump(lent_list)

    return jsonify(data.data)


@mod_api.route('/<facility>/ical/lent.ics', methods=['GET'])
@valid_facility
@valid_token
def lent_ical(facility):
    """Returns a calendar for all lent items in the ical format.

    The calendar file includes all return dates for all lent items. It can be
    used for importing them into other calendar software like the
    Google calendar or Thunderbird Lightning.

    Request::

        http GET localhost:5000/api/wolfsburg/ical/lent.ics?token=pIUBfh1se

    Response::

        BEGIN:VCALENDAR
        PRODID:ics.py - http://git.io/lLljaA
        VERSION:2.0
        BEGIN:VEVENT
        DTSTAMP:20160609T101434Z
        DTSTART:20160415T000000Z
        SUMMARY:Bibliotheksrueckgaben: 2
        DESCRIPTION:Dürer\, Albrecht: Albrecht Dürer\\nHopper\, Edward: Edward
        UID:7a3fcb35-2cb4-48d3-ab56-2cf62af04337@7a3f.org
        END:VEVENT
        BEGIN:VEVENT
        DTSTAMP:20160609T101434Z
        DTSTART:20160420T000000Z
        SUMMARY:Bibliotheksrueckgaben: 1
        DESCRIPTION:Hopkins\, John: Modezeichnen
        UID:86474116-dfd6-408f-9c2b-2e2cb552ab9b@8647.org
        END:VEVENT
        END:VCALENDAR

    :param facility: The facility to get a lent list from.
    :type facility: str

    """
    s = URLSafeSerializer(current_app.config['SECRET_KEY'], salt=facility)

    token = request.args['token']

    # check if token already in redis
    redis_entry = g.redis.hgetall(token)
    if redis_entry:

        two_hours_ago = arrow.utcnow().replace(hours=-2)
        updated = arrow.get(redis_entry[b'updated'].decode('utf-8'))

        if updated > two_hours_ago:
            ical = redis_entry[b'ical'].decode('utf-8')

            return Response(ical, mimetype='text/calendar')

    userdata = s.loads(token)

    lent_list = current_app.facilities[facility]['lent_list'](
        userdata['username'], userdata['password'])

    data = schemes.LentListResponse().dump(lent_list)

    ical = build_ical(data.data)

    # store new ical in redis
    g.redis.hmset(token, dict(ical=ical, updated=arrow.utcnow()))

    return Response(ical, mimetype='text/calendar')
