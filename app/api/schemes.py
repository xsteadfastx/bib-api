from marshmallow import Schema, fields


class Copy(Schema):
    """Schema for an individual copy.

    A title has one or more items in a library.
    """
    available = fields.Boolean()
    branch = fields.String()
    due_date = fields.Date()
    id = fields.String()
    position = fields.String()
    type = fields.String()


class Title(Schema):
    """Schema for a library title.

    A title has one or more copies in a library.
    """
    annotation = fields.String()
    author = fields.String()
    cover = fields.URL()
    isbn = fields.String()
    copies = fields.Nested(Copy, many=True)
    title = fields.String()
    year = fields.Date()


class SearchRequest(Schema):
    """ Schema for a search request."""
    term = fields.String(required=True)


class SearchResponse(Schema):
    """ Schema for a search result."""
    results = fields.Nested(Title, many=True)
    next_page = fields.Int()
