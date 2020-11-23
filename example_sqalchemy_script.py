from emannotationschemas.models import make_annotation_model, Base
from emannotationschemas.flatten import flatten_dict
from emannotationschemas import get_schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# example of initializing mapping of database
DATABASE_URI = "postgres://postgres:synapsedb@localhost:5432/minnie"
engine = create_engine(DATABASE_URI, echo=True)
model_dict = make_annotation_model('test', 'synapse')
# assures that all the tables are created
# would be done as a db management task in general
Base.metadata.create_all(engine)

# create a session class
# this will produce session objects to manage a single transaction
Session = sessionmaker(bind=engine)

# some example test data as a raw json compatible blob
synapse_d = {
    "type": "synapse",
    "pre_pt":
    {
        "position": [5, 5, 10],
        "root_id": 9223372036854775899,
        "supervoxel_id": 89851029364932800
    },
    "post_pt":
    {
        "position": [10, 5, 10],
        "root_id": 9223372036854775898,
        "supervoxel_id": 106205165316472881
    },
    "ctr_pt": {
        "position": [7, 5, 10]
    },
    "size": 40.5
}
# get the schema to deserialize the test data
SynapseSchema = get_schema('synapse')
schema = SynapseSchema(context={'postgis': True})

# use the schema to deserialize the schema
d = schema.load(synapse_d)
d = flatten_dict(d)

# get the appropriate sqlalchemy model
# for the annotation type and dataset
SynapseModel = model_dict['test']['synapse']

# # create a new model instance with data
synapse = SynapseModel(**d)

# # create a new db session
session = Session()
# add this synapse to database
session.add(synapse)
# commit this transaction to database
session.commit()
