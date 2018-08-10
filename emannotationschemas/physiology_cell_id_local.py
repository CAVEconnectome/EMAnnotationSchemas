from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm

class PhysiologyCellIdLocal( AnnotationSchema ):

    cell_id = mm.fields.Int( 
                required=True,
                description='Cell id in calcium data')
    pt = mm.fields.Nested( BoundSpatialPoint, 
                required=True,
                description='Location of physiology ROI')

    @mm.post_load
    def validate_type( self, item):
        assert item['type'] == 'physiology_cell_id'