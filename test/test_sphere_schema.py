from emannotationschemas.bound_sphere import BoundSphere

good_sphere = {'type':'sphere',
             'ctr_pt':{'position':[1000,1000,1000]},
             'radius':20}

bad_sphere = {'type':'sphere',
            'ctr_pt':{'position':[1000,1000,1000]},
            'radius':-20}

def annotation_import(item):
    item['supervoxel_id'] = 5
    item.pop('rootId', None)

def test_sphere_validation():
    schema = BoundSphere(context={'bsp_fn':annotation_import})
    result = schema.load(good_sphere)
    assert result.data['ctr_pt']['supervoxel_id'] == 5
    assert result.data['valid']

    result = schema.load(bad_sphere)
    assert not result.data['valid']