def CategoricalValidationFactory(allowed_category_dict):
    def categorical_validation(item):
        for category_name, allowed_categories in allowed_category_dict.items():
            if item[category_name] not in allowed_categories:
                return False
        else:
            return True
    return categorical_validation

def NonequalRootIDValidationFactory(nonequal_pair):
    def nonequal_validation(item):
        ptA = item[nonequal_pair[0]].get('root_id', None)
        ptB = item[nonequal_pair[1]].get('root_id', None)
        if ptA == ptB:
            if ptA is not None:
                return False
            else:
                return None
        else:
            return True
    return nonequal_validation

validation_func_lookup = {
    'nonequal_root_id': NonequalRootIDValidationFactory,
    'categorical': CategoricalValidationFactory,
    }
