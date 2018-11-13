from emannotationschemas.models import Base, format_table_name, annotation_models, root_model_name
from sqlalchemy import Column, String, Integer, Float, Numeric, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
compartment_model_name = "NeuronCompartment"
post_synaptic_compartment_name = "PostSynapseCompartment"


def make_neuron_compartment_model(dataset, version: int = 1):
    compartment_type = compartment_model_name.lower()

    root_id_name = format_table_name(dataset,
                                     root_model_name.lower(),
                                     version)+'.id'

    attr_dict = {
        '__tablename__': format_table_name(dataset,
                                           compartment_model_name.lower(),
                                           version=version),
        'vertices': Column(LargeBinary),
        'labels': Column(LargeBinary),
        'root_id': Column(Numeric, ForeignKey(root_id_name), primary_key=True)
    }
    model_name = dataset.capitalize() + compartment_model_name

    if not annotation_models.contains_model(dataset,
                                            compartment_type,
                                            version=version):
        annotation_models.set_model(dataset,
                                    compartment_type,
                                    type(model_name, (Base,), attr_dict),
                                    version=version)
    return annotation_models.get_model(dataset,
                                       compartment_type,
                                       version=version)


def make_post_synaptic_compartment_model(dataset,
                                         synapse_table,
                                         version: int = 1):

    psc_name_lower = post_synaptic_compartment_name.lower()
    synapse_model_name = dataset.capitalize()+ compartment_model_name
    synapse_table_name = format_table_name(dataset, synapse_table, version=version)

    attr_dict = {
        '__tablename__': format_table_name(dataset,
                                           psc_name_lower,
                                           version=version),
        'label': Column(Integer),
        'synapse_id': Column(Numeric, ForeignKey(synapse_table_name + ".id"), primary_key=True)
    }
    model_name = dataset.capitalize() + post_synaptic_compartment_name
    if not annotation_models.contains_model(dataset,
                                            psc_name_lower,
                                            version=version):
        annotation_models.set_model(dataset,
                                    psc_name_lower,
                                    type(model_name, (Base,), attr_dict),
                                    version=version)

    return annotation_models.get_model(dataset,
                                       psc_name_lower,
                                       version=version)
