from mock import patch, Mock
from tinifyUrl.service import string_to_code


# Object for mocking redis functions used by us.


class MockRedis():
    mock_get_return = None

    def get(self, val):
        if self.mock_get_return:
            return self.mock_get_return.encode('utf-8')
        return None

    def set(self, *args, **kwargs):
        return None


# Tinify URL View.


def test_tinify_url_works(client):
    url = '/shorten-url'
    url_to_shorten = 'mytesturl.com'
    with patch('tinifyUrl.service.get_redis') as mock:
        mock.return_value = MockRedis()
        response = client.post(url, json={'url': url_to_shorten})
    assert response.status_code == 200
    assert response.json['code'] == string_to_code(url_to_shorten)


def test_tinify_url_key_taken_by_same_url(client):
    url = '/shorten-url'
    url_to_shorten = 'mytesturl.com'

    mock_redis = MockRedis()
    mock_redis.mock_get_return = url_to_shorten
    with patch('tinifyUrl.service.get_redis') as mock:
        mock.return_value = mock_redis
        response = client.post(url, json={'url': url_to_shorten})
    assert response.status_code == 200
    assert response.json['code'] == string_to_code(url_to_shorten)


def test_tinify_url_key_taken_by_different_url(client):
    url = '/shorten-url'
    url_to_shorten = 'mytesturl.com'

    mock_redis = MockRedis()
    mock_redis.get = Mock()
    mock_redis.get.side_effect = ['someotherurl.com'.encode('utf-8'), None]
    with patch('tinifyUrl.service.get_redis') as mock:
        mock.return_value = mock_redis
        response = client.post(url, json={'url': url_to_shorten})
    assert response.status_code == 200
    assert response.json['code'] is not None


def test_tinify_url_collides_too_often(client):
    url = '/shorten-url'
    url_to_shorten = 'mytesturl.com'
    mock_redis = MockRedis()
    mock_redis.mock_get_return = 'someotherurl.com'
    with patch('tinifyUrl.service.get_redis') as mock:
        mock.return_value = mock_redis
        response = client.post(url, json={'url': url_to_shorten})
    assert response.status_code == 400
    assert 'Please try again later' in str(response.data)


# # Expand URL view.


def test_expand_url_works(client):
    url = '/expand-url'
    code_to_expand = 'tstcode'
    expected_url = 'mytesturl.com'
    mock_redis = MockRedis()
    mock_redis.mock_get_return = expected_url
    with patch('tinifyUrl.service.get_redis') as mock:
        mock.return_value = mock_redis
        response = client.post(url, json={'code': code_to_expand})
    assert response.status_code == 200
    assert response.json['url'] == expected_url


def test_expand_url_not_found(client):
    url = '/expand-url'
    code_to_expand = 'tstcode'
    with patch('tinifyUrl.service.get_redis') as mock:
        mock.return_value = MockRedis()
        response = client.post(url, json={'code': code_to_expand})
    assert response.status_code == 404
