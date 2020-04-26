from datetime import datetime
import pytest
import marshmallow

from src.schemas import LogSchema


def test_good_schema():
    schema = LogSchema()

    data = schema.load({
                        'client_id': 'user_id',
                        'User-Agent': 'Firefox 80',
                        'document.location': 'http://www.google.com/ref?data=1',
                        'document.referer': 'http://www.google.com/ref?data=2',
                        'date': '2020-12-01T02:03:50.31232'
                       })
    assert data['client_id' ] == 'user_id'
    assert data['user_agent'] == 'Firefox 80'
    assert data['location'] == 'http://www.google.com/ref?data=1'
    assert data['referer'] == 'http://www.google.com/ref?data=2'
    assert data['date'] == datetime(2020, 12, 1, 2, 3, 50, 312320)

    data = schema.load({
                        'client_id': '',
                        'User-Agent': '',
                        'document.location': 'http://www.google.com/ref?data=1',
                        'document.referer': '',
                        'date': '2020-12-01T02:03:50.31232',
                       })
    assert data['client_id' ] == ''
    assert data['user_agent'] == ''
    assert data['location'] == 'http://www.google.com/ref?data=1'
    assert data['referer'] == ''
    assert data['date'] == datetime(2020, 12, 1, 2, 3, 50, 312320)

    data = schema.load({
                        'client_id': '',
                        'User-Agent': '',
                        'document.location': 'http://www.google.com/ref?data=1',
                        'document.referer': 'some shit',
                        'date': '2020-12-01T02:03:50.31232',
                       })
    assert data['client_id' ] == ''
    assert data['user_agent'] == ''
    assert data['location'] == 'http://www.google.com/ref?data=1'
    assert data['referer'] == ''
    assert data['date'] == datetime(2020, 12, 1, 2, 3, 50, 312320)


@pytest.mark.parametrize("input_data", [{
                                          'client_id': 'user_id',
                                          'User-Agent': 'Firefox 80',
                                          'document.location': 'http://www.google.com/ref?data=1',
                                          'document.referer': 'http://www.google.com/ref?data=2',
                                          'date': '2020-12-01T02:03:50.31232',
                                          'sth': 'sth2'
                                        },
                                        {
                                          'client_id': 'user_id',
                                          'document.location': 'http://www.google.com/ref?data=1',
                                          'document.referer': 'http://www.google.com/ref?data=2',
                                          'date': '2020-12-01T02:03:50.31232'
                                        },{
                                          'client_id': 'user_id',
                                          'User-Agent': 'Firefox 80',
                                          'document.location': 'http://www.google.com/ref?data=1',
                                          'document.referer': 'http://www.google.com/ref?data=2',
                                          'date': '2020-13-01T02:03:50.31232'
                                        }
                                        ])
def test_bad_schema(input_data):
    with pytest.raises(marshmallow.exceptions.ValidationError) as excinfo:
        schema = LogSchema()
        data = schema.load(input_data)
