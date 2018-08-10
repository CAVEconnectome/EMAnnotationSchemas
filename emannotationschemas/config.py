import json

def import_config( schema_config_file ):
    try:
        type_mapping = dict()
        with open(schema_config_file, 'r') as fid:
            type_config = json.load(fid)
            for type in type_config:
                if isinstance(type_config, dict):
                    if type not in type_mapping.keys():
                        sm = type_config[type].split('.')
                        exec('from emannotationschemas.{} import {}'.format(sm[0],sm[1]))
                        exec('type_mapping[\'{}\'] = {}'.format(type, sm[1]) )
                    else:
                        raise Warning('{} defined multiple times in the schema config.'
                                    ' Using only the first instance'.format(type))
        if len( type_mapping ) == 0:
            raise Warning('No schema were imported!')
        return type_mapping
    except FileNotFoundError:
        msg = 'No schema_config.json file found.'
        raise FileNotFoundError(msg)
    except NameError:
        raise
