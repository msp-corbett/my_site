class APIError(Exception):
    """ Exception to raise when API call errors

    Attributes:
        error_code -- HTML response error code to pass back.
        error_source -- value where the error occured.
    """

    def __init__(self, error_code, error_source):
        self.error_code = error_code
        self.error_source = error_source


def filter_query(query, raw_filters, model):
    """
        Modified version of accpeted answer from:
        https://stackoverflow.com/questions/14845196/dynamically-constructing-filters-in-sqlalchemy

        1 - Split the desired filters out from filters url argument
        2 - split each filter into the Column corresponding to the Model.Column, the filter operator and the search value
        3 - using a lambda funciton create corresponding SQLAlchemy ORM Internal
          - https://docs.sqlalchemy.org/en/13/orm/internals.html
        4 - Create and chain the filter(s) to the query.

        Example:
        import requests
        r = requests.get('http://server/api/user?filters=FirstName eq "Jimmy" AND LastName eq "Bob")
    """
    for filter_ in raw_filters.split(' AND '):
        try:
            key, op, value = filter_.split(' ', maxsplit=2)
        except ValueError:
            raise APIError(400, f'Invalid filter: {filter_}')

        value = value.strip("'")
        value = value.strip('"')

        column = getattr(model, key, None)
        if not column:
            raise APIError(400, f'Invalid field: {key}')

        if op == 'in':
            values = value.split(',')
            values = [v.strip(' ') for v in values]
            filt = column.in_(values)
        else:
            try:
                attr = list(filter(lambda e: hasattr(column, f"{e}"), [f'{op}', f'{op}_', f'__{op}__']))[0]
            except IndexError:
                raise APIError(400, f'Invalid operation: {op}')
            if value == 'null':
                value = None

        filt = getattr(column, attr)(value)
        query = query.filter(filt)
    return query