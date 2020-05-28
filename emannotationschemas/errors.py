class UnknownAnnotationTypeException(Exception):
    '''exception raised when an unknown schema is asked for '''


class InvalidTableMetaDataException(Exception):
    '''exception is raised when metadata for a table is not valid or is missing'''


class InvalidSchemaField(Exception):
    '''Exception raised if a schema can't be translated to a model'''