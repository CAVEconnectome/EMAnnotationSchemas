import marshmallow as mm
from emannotationschemas.schemas.base import AnnotationSchema, BoundSpatialPoint


class BoundTagAnnotation(AnnotationSchema):
    pt = mm.fields.Nested(
        BoundSpatialPoint, required=True, description="Location associated with the tag"
    )
    tag = mm.fields.String(required=True, description="Arbitrary text tag")


class BoundDoubleTagAnnotation(BoundTagAnnotation):
    tag2 = mm.fields.String(required=True, description="Arbitrary text tag")


class Bound2TagAnnotation(BoundTagAnnotation):
    pt2 = mm.fields.Nested(
        BoundSpatialPoint, required=True, description="Location associated with the tag"
    )
    tag2 = mm.fields.String(required=True, description="Arbitrary text tag")


class BoundTagAnnotationUser(BoundTagAnnotation):
    user_id = mm.fields.Int(required=True, description="User who created the tag.")


class BoundDoubleTagAnnotationUser(BoundDoubleTagAnnotation):
    user_id = mm.fields.Int(
        required=True,
        description=f"User who created the tag.",
    )


class Bound2TagAnnotationUser(Bound2TagAnnotation):
    user_id = mm.fields.Int(required=True, description="User who created the tag.")
