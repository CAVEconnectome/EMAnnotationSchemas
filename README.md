[![Build Status](https://www.travis-ci.com/fcollman/EMAnnotationSchemas.svg?branch=master)](https://www.travis-ci.com/fcollman/EMAnnotationSchemas)
# EMAnnotationSchemas
Repository to hold schemas for annotations of volumetric imaging data focused on EM

# How to add a new annotation type
In order to add a new annotation type to this repository you must do the following steps.

1. Create a new schema for your annotation.    This schema needs to follow a few guidelines.
  * This schema should extend the class [AnnotationSchema](emannotationschemas/base.py).
  * The central tenant of annotations, is that you should mark spatial locations that should be linked to agglomerated objects in the segmented EM volume with a [BoundSpatialPoint](emannotationschemas/base.py) nested schema.  This will announce to the [AnnotationEngine](http://www.github.com/fcollman/AnnotationEngine) and the [MaterializationEngine](http://www.github.com/seung-lab/MaterializationEngine) that the associated root_ids  (neurons/glia/axon fragment/etc) should be "bound" to these locations and easily referenced (along with the nearest skeleton node and mesh node).  You may also include points which do not need to be linked to root_ids, as [SpatialPoints](emannotationschemas/base.py) (of which BoundSpatialPoint is a subclass).  All Nested SpatialPoint fields can include an 'order' keyword, which will be used by UI elements to determine whether, and in what order to draw lines between these points to represent an annotation. 
2. Import this schema into [__init__.py](emannotationschemas/__init__.py), and add the schema to the type_mapping dictionary, giving it a string based key.  This will be the annotation_type of your new class of annotation. 

An example of a proper schema is [SynapseSchema](emannotationschemas/synapse.py). 
