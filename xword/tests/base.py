import json
import pytest
from uuid import uuid4
from urllib import urlencode


class ViewTestCaseResponse(object):
    """Wraps a response object to easily extract and manipulate fields."""
    @pytest.fixture(scope='function', autouse=True)
    def headers(self):
        return {'Content-Type': 'application/json'}

    def __init__(self, response):
        self.data = json.loads(response.get_data() or '{}')
        self.status_code = response.status_code


class TestView(object):
    def _get_headers(self, headers, new_headers):
        """Get headers to send with the request."""
        default_headers = headers
        default_headers.update(new_headers)
        return default_headers

    def post(self, url, client, headers, data=None, **kwargs):
        """Perform a post request."""
        headers = self._get_headers(headers, kwargs.pop('headers', {}))
        data = json.dumps(data) if headers.get('Content-Type') == 'application/json' else data
        res = client.post(
            url,
            data=data,
            headers=headers,
            **kwargs
        )
        return ViewTestCaseResponse(res)

    def raw_get(self, url, client, headers, **kwargs):
        """Perform a get request with no additional formatting."""
        res = client.get(
            url,
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
            **kwargs
        )
        return res

    def get(self, client, url, headers, params=None, **kwargs):
        """Perform a get request."""
        param_string = '?{}'.format(urlencode(params)) if params else ''
        res = client.get(
            '{}{}'.format(url, param_string),
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
            **kwargs
        )
        return ViewTestCaseResponse(res)

    def delete(self, client, url, headers, **kwargs):
        """Perform a delete request."""
        res = client.delete(
            url,
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
            **kwargs
        )
        return ViewTestCaseResponse(res)

    def patch(self, client, url, headers, data=None, **kwargs):
        """Perform a patch request."""
        res = client.patch(
            url,
            data=json.dumps(data),
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
            **kwargs
        )
        return ViewTestCaseResponse(res)


class TestCRUD(TestView):

    def _get_headers(self, headers, new_headers):
        """Get headers to send with the request."""
        default_headers = headers
        default_headers.update(new_headers)
        return default_headers

    def _assert_equal(self, expected, result):
        for k in expected:
            if k == 'phone_number' and expected[k] is not None and result[k] is not None:
                assert PhoneNumber(expected[k]).e164 == result[k], 'Failed key={}'.format(k)
            else:
                assert expected[k] == result[k], 'Failed key={}'.format(k)

    def _test_post(self, model_factory, url_prefix, client, headers):
        """Test that we can create a new record."""
        attrs = model_factory.build()
        del attrs['id']
        res = self.post(
            client=client,
            headers=headers,
            url='/{}/'.format(url_prefix),
            data=attrs,
        )
        assert res.status_code == 201
        self._assert_equal(attrs, res.data)

    def _test_get(self, model_factory, url_prefix, client, headers, **kwargs):
        """Test that we can get a record."""
        record = model_factory()
        res = self.get(
            url='/{}/{}'.format(
                url_prefix,
                record.id,
            ),
            client=client,
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
        )
        assert res.data['id'] == record.id
        assert res.status_code == 200

    def _test_get_404(self, url_prefix, client, headers, **kwargs):
        """Test that we can get a record 404's."""
        res = self.get(
            client=client,
            url='/{}/{}'.format(
                url_prefix,
                uuid4().hex,
            ),
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
        )
        assert res.status_code == 404

    def _test_get_soft_deleted(self, url_prefix, model_factory, client, headers, **kwargs):
        """Test that we can get a record."""
        record = model_factory()
        record.deleted_at = standard_datetime.now()
        res = self.get(
            url='/{}/{}'.format(
                url_prefix,
                str(record.id)
            ),
            client=client,
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
        )
        assert res.status_code == 404, 'FAILURE: {}'.format(res.status_code)

    def _test_get_list(self, model, model_factory, url_prefix, client, headers, **kwargs):
        """Test that we can get a record."""
        records = model_factory.create_batch(size=3)
        res = self.get(
            client=client,
            url='/{}/'.format(url_prefix),
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
        )
        assert res.status_code == 200
        found = model.query.all()
        assert len(found) == 3
        found = sorted(found, key=lambda p: p.id)
        records = sorted(records, key=lambda p: p.id)
        for i, f in enumerate(found):
            assert found[i].id == records[i].id

    def _test_get_list_soft_deleted(self, model_factory, url_prefix, client, headers, **kwargs):
        """Test that we can get a record."""
        records = model_factory.create_batch(size=3)
        for record in records:
            record.deleted_at = standard_datetime.now()
        res = self.get(
            url='/{}/'.format(url_prefix),
            client=client,
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
        )
        assert res.status_code == 200
        assert not res.data

    def _test_delete(self, model, model_factory, url_prefix, client, headers, **kwargs):
        """Test that we can delete a record."""
        record = model_factory()
        results = len(model.query.all())
        assert results == 1, 'FAILURE: {}'.format(results)
        res = self.delete(
            url='/{}/{}'.format(url_prefix, str(record.id)), client=client,
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
        )
        found = model.query.all()
        assert len(found) == 1
        assert found[0].deleted_at is not None
        assert res.status_code == 204
        assert not res.data

    def _test_patch(self, model_factory, url_prefix, client, headers, **kwargs):
        """Test that we can patch a record."""
        record = model_factory()
        expected = model_factory.build()
        for rel in record.relationships(key_delim='_'):
            expected[rel] = getattr(record, rel)
        del expected['id']

        data = {
            'data': {
                'attributes': expected,
                'type': '{}'.format(url_prefix),
                'id': record.id,
            }
        }
        res = self.patch(
            client=client,
            url='/{}/{}'.format(url_prefix, record.id),
            data=data,
            headers=self._get_headers(headers, kwargs.pop('headers', {})),
        )
        assert res.status_code == 200
        self._assert_equal(expected, res.data)
