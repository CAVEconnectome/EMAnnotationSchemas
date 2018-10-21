from emannotationschemas.blueprint_app import __version__


def test_index(client):
    response = client.get('/schema')
    assert(response.status_code == 200)


def test_version(client):
    response = client.get('/schema/version')
    assert(response.status_code == 200)
    assert(response.json == __version__)


def test_types(client):
    response = client.get('/schema/type')
    assert response.status_code == 200
    assert type(response.json) == list


def test_bad_schema(client):
    response = client.get('/schema/type/not_a_type')
    print(response.data)
    assert(response.status_code == 404)


def test_get_synapse_schema(app, client):
    url = '/schema/type/synapse'.format()
    response = client.get(url)
    assert(response.status_code == 200)
    assert(len(response.data) > 0)
    schema = response.json
    assert('$ref' in schema.keys())
    assert('#/definitions/SynapseSchema' in schema['$ref'])
    assert('SynapseSchema' in schema['definitions'])
    assert('pre_pt' in schema['definitions']['SynapseSchema']['properties'])
    assert('post_pt' in schema['definitions']['SynapseSchema']['properties'])