from emannotationschemas.blueprint_app import __version__


def test_types(client):
    response = client.get('/schema/api/v2/type')
    assert response.status_code == 200
    assert type(response.json) == list


def test_bad_schema(client):
    response = client.get('/schema/api/v2/type/not_a_type')
    print(response)
    assert(response.status_code == 404)


def test_get_synapse_schema(app, client):
    url = '/schema/api/v2/type/synapse'.format()
    response = client.get(url)
    assert(response.status_code == 200)
    schema = response.json
    assert(len(schema) > 0)
    assert('$ref' in schema.keys())
    assert('#/definitions/SynapseSchema' in schema['$ref'])
    assert('SynapseSchema' in schema['definitions'])
    assert('pre_pt' in schema['definitions']['SynapseSchema']['properties'])
    assert('post_pt' in schema['definitions']['SynapseSchema']['properties'])