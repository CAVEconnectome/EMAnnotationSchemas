class UnknownAnnotationTypeException(Exception):
    '''exception raised when an unknown schema is asked for '''


class InvalidTableMetaDataException(Exception):
    '''exception is raised when metadata for a table is not valid or is missing'''