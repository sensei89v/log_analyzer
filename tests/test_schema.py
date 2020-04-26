from datetime import datetime
import pytest
import marshmallow

from src.schemas import LogSchema

# TODO. Add check fix referer
@pytest.mark.parametrize("input_data", [{
                                          'client_id': 'user_id',
                                          'User-Agent': 'Firefox 80',
                                          'document.location': 'http://www.google.com/ref?data=1',
                                          'document.referer': 'http://www.google.com/ref?data=2',
                                          'date': '2020-12-01T02:03:50.31232'
                                        },
                                        {
                                          'client_id': '',
                                          'User-Agent': '',
                                          'document.location': 'http://www.google.com/ref?data=1',
                                          'document.referer': '',
                                          'date': '2020-12-01T02:03:50.31232',
                                        },
                                        {
                                          'client_id': '',
                                          'User-Agent': '',
                                          'document.location': 'http://www.google.com/ref?data=1',
                                          'document.referer': 'some shit',
                                          'date': '2020-12-01T02:03:50.31232',
                                        }])
def test_good_schema(input_data):
    schema = LogSchema()
    data = schema.load(input_data)
    assert 'client_id' in data
    assert 'user_agent'  in data
    assert 'location'  in data
    assert 'referer' in data
    assert 'date' in data


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
