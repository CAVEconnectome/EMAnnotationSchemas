[![Actions Status](https://github.com/seung-lab/EMAnnotationSchemas/workflows/EMAnnotationSchemas/badge.svg)](https://github.com/seung-lab/EMAnnotationSchemas/actions)
[![codecov](https://codecov.io/gh/seung-lab/EMAnnotationSchemas/branch/master/graph/badge.svg)](https://codecov.io/gh/seung-lab/EMAnnotationSchemas)

# EMAnnotationSchemas
Repository to hold schemas for annotations of volumetric imaging data focused on EM

# How to add a new annotation type
In order to add a new annotation type to this repository you must do the following steps.

1. Create a new schema for your annotation.    This schema needs to follow a few guidelines.
  * This schema should extend the class [emannotationschemas.schemas.base.AnnotationSchema](emannotationschemas/schemas/base.py).
  * The central tenant of annotations, is that you should mark spatial locations that should be linked to agglomerated objects in the segmented EM volume with a [emannotationschemas.schemas.base.BoundSpatialPoint](emannotationschemas/schemas/base.py) nested schema.  This will announce to the [AnnotationEngine](http://www.github.com/fcollman/AnnotationEngine) and the [MaterializationEngine](http://www.github.com/seung-lab/MaterializationEngine) that the associated root_ids  (neurons/glia/axon fragment/etc) should be "bound" to these locations and easily referenced (along with the nearest skeleton node and mesh node).  You may also include points which do not need to be linked to root_ids, as [emannotationschemas.schemas.base.SpatialPoint](emannotationschemas/schemas/base.py) (of which BoundSpatialPoint is a subclass).  All Nested SpatialPoint fields can include an 'order' keyword, which will be used by UI elements to determine whether, and in what order to draw lines between these points to represent an annotation. 
   * If your annotation needs to reference another annotation.  For example, if you want to be able to annotate that a certain synapse is of a certain type, or that a spine head is dually innervated, then you should subclass a [emannotationschemas.schemas.base.ReferenceAnnotation](emannotationschemas/schemas/base.py), so the system knows to link that annotation to its reference annotation.
   * You should add a mm.post_load validation methods to the schema that ensure everything is what you would expect. For example that the type field is what you want it to be, and that any reference_annotation_type are what they should be. It should set the 'valid' flag of the annotation when the necessary information to validation the annotation is present, and remove that key from the dictionary when the information is not yet present.  For example, upon posting new annotations to the annotationengine, root_id's are not available, and so synapses cannot be 'valid' based upon their having different pre/post IDs, but later, when materialized, they should have those IDs.
2. Import this schema into [__init__.py](emannotationschemas/__init__.py), and add the schema to the type_mapping dictionary, giving it a string based key.  This will be the annotation_type of your new class of annotation. 

3. You should add a test to the [testing suite](tests/) that uses this schema, and checks that you can correctly detect potential problems with annotation data that is sent into the system. 

An example of a proper schema is [emannotationschemas.schemas.synapse.SynapseSchema](emannotationschemas/schemas/synapse.py).
