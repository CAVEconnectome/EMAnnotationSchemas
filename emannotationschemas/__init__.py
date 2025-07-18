from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.flatten import create_flattened_schema
from emannotationschemas.schemas.base import (
    FlatSegmentationReferenceSinglePoint,
    ReferenceAnnotation,
    ReferenceInteger,
    ReferenceTagAnnotation,
    ReferenceTagWithConfidence,
    RepresentativePoint,
)
from emannotationschemas.schemas.bound_bool_tag import (
    BoundBoolAnnotation,
    BoundBoolWithValid,
    BoundTagWithValid,
    SpatialPointBoolWithValid,
)
from emannotationschemas.schemas.bound_text_tag import (
    Bound2TagAnnotation,
    Bound2TagAnnotationUser,
    BoundDoubleTagAnnotation,
    BoundDoubleTagAnnotationUser,
    BoundTagAnnotation,
    BoundTagAnnotationUser,
)
from emannotationschemas.schemas.bouton_shape import BoutonShape
from emannotationschemas.schemas.braincircuits import (
    BrainCircuitsBoundTagAnnotationUser,
)
from emannotationschemas.schemas.cell_type_local import CellTypeLocal, CellTypeReference
from emannotationschemas.schemas.contact import Contact
from emannotationschemas.schemas.derived_spatial_point import (
    DerivedNumeric,
    DerivedSpatialPoint,
    DerivedTag,
)
from emannotationschemas.schemas.extended_classical_cell_type import (
    ExtendedClassicalCellType,
)
from emannotationschemas.schemas.fly_cell_types import FlyCellType, FlyCellTypeExt
from emannotationschemas.schemas.functional_coregistration import (
    FunctionalCoregistration,
    FunctionalUnitCoregistration,
    FunctionalUnitCoregistrationExtended,
    V1DDFunctionalUnitCoregistration,
)
from emannotationschemas.schemas.functional_props import FunctionalPropertiesBCM
from emannotationschemas.schemas.glia_contact import GliaContact
from emannotationschemas.schemas.groups import SimpleGroup
from emannotationschemas.schemas.neuropil import FlyNeuropil
from emannotationschemas.schemas.nucleus_detection import NucleusDetection
from emannotationschemas.schemas.postsynaptic_compartment import PostsynapticCompartment
from emannotationschemas.schemas.presynaptic_bouton_type import PresynapticBoutonType
from emannotationschemas.schemas.proofreading import (
    CompartmentProofreadStatus,
    CompartmentProofreadStatusStrategy,
    ProofreadingBoolStatusUser,
    ProofreadStatus,
)
from emannotationschemas.schemas.reference_text_float import (
    ReferenceTagFloat,
)
from emannotationschemas.schemas.synapse import (
    BuhmannEcksteinSynapseSchema,
    BuhmannSynapseSchema,
    NoCenterSynapse,
    NoCleftSynapse,
    PlasticSynapse,
    SynapseSchema,
    ValidSynapse,
)

__version__ = "5.23.0"

type_mapping = {
    "synapse": SynapseSchema,
    "nocleft_synapse": NoCleftSynapse,
    "nocenter_synapse": NoCenterSynapse,
    "fly_synapse": BuhmannSynapseSchema,
    "fly_nt_synapse": BuhmannEcksteinSynapseSchema,
    "bouton_shape": BoutonShape,
    "presynaptic_bouton_type": PresynapticBoutonType,
    "postsynaptic_compartment": PostsynapticCompartment,
    "microns_func_coreg": FunctionalCoregistration,
    "microns_func_unit_coreg": FunctionalUnitCoregistration,
    "v1dd_func_unit_coreg": V1DDFunctionalUnitCoregistration,
    "func_unit_ext_coreg": FunctionalUnitCoregistrationExtended,
    "func_properties_bcm": FunctionalPropertiesBCM,
    "simple_reference": ReferenceAnnotation,
    "reference_tag": ReferenceTagAnnotation,
    "cell_type_local": CellTypeLocal,
    "cell_type_reference": CellTypeReference,
    "nucleus_detection": NucleusDetection,
    "bound_tag": BoundTagAnnotation,
    "bound_double_tag": BoundDoubleTagAnnotation,
    "bound_2tag": Bound2TagAnnotation,
    "bound_tag_user": BoundTagAnnotationUser,
    "bound_double_tag_user": BoundDoubleTagAnnotationUser,
    "bound_2tag_user": Bound2TagAnnotationUser,
    "extended_classical_cell_type": ExtendedClassicalCellType,
    "plastic_synapse": PlasticSynapse,
    "glia_contact": GliaContact,
    "contact": Contact,
    "derived_spatial_point": DerivedSpatialPoint,
    "derived_tag": DerivedTag,
    "derived_numeric_value": DerivedNumeric,
    "proofread_status": ProofreadStatus,
    "compartment_proofread_status": CompartmentProofreadStatus,
    "proofreading_boolstatus_user": ProofreadingBoolStatusUser,
    "fly_neuropil": FlyNeuropil,
    "reference_point": FlatSegmentationReferenceSinglePoint,
    "representative_point": RepresentativePoint,
    "reference_synapse_valid": ValidSynapse,
    "reference_simple_group": SimpleGroup,
    "fly_cell_type": FlyCellType,
    "fly_cell_type_ext": FlyCellTypeExt,
    "braincircuits_annotation_user": BrainCircuitsBoundTagAnnotationUser,
    "bound_tag_bool": BoundBoolAnnotation,
    "bound_tag_bool_valid": BoundBoolWithValid,
    "bound_tag_valid": BoundTagWithValid,
    "pt_bool_valid": SpatialPointBoolWithValid,
    "reference_integer": ReferenceInteger,
    "reference_tag_float": ReferenceTagFloat,
    "compartment_proofread_status_strategy": CompartmentProofreadStatusStrategy,
    "reference_tag_with_confidence": ReferenceTagWithConfidence,
}


def get_types():
    return [k for k in type_mapping.keys()]


def get_schema(schema_type: str):
    """Get schema class object by keyword, only
    returns an object that is listed in :data:`type_mapping` dict

    Parameters
    ----------
    schema_type : str
        Key name of schema in :data:`type_mapping`

    Returns
    -------
    obj
        marshmallow schema object

    Raises
    ------
    UnknownAnnotationTypeException
        Key argument is not in :data:`type_mapping` dict
    """
    try:
        return type_mapping[schema_type]
    except KeyError:
        msg = f"Schema type: {schema_type} is not a known annotation type"
        raise UnknownAnnotationTypeException(msg)


def get_flat_schema(schema_type: str):
    try:
        Schema = type_mapping[schema_type]
        return create_flattened_schema(Schema)
    except KeyError as e:
        msg = f"Schema type: {schema_type} is not a known annotation type: {e}"
        raise UnknownAnnotationTypeException(msg)
