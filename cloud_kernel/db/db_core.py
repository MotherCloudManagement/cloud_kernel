from cloud_kernel.db import DatabaseSession, CLOUD_KERNEL_ENGINE_STRING
from inspect import isclass
import zlib

class LoadTables(object):
    """
    Load all tables in Database that will be used for storing Values.
    The Table Names will be the same as the trigger class names.

    """
    @staticmethod
    def LoadTableNames():
        tablenames = []

        try:
            global_triggers = globals().copy()
            for x, y in global_triggers.items():
                if not isclass(y):
                    continue
                # TODO continue looking into the __subclasscheck__ to filter these out cleaner
                if x in ['CloudKernelTriggerBase', 'Mapping', 'FetchStaticTriggers', 'FetchProducedJobs']:
                    continue
                tablenames.append(y)
        except Exception as e:
            pass

        return tablenames


def install(self, model):
    def make_content_type_id(model):
        mname = model.__name__
        tname = model.__table__.name
        return zlib.crc32("{0}/{1}".format(mname, tname), 0) & 0xffffffff

    def tracked_record(object):
        def __settattr__(self, *args):
            raise AttributeError("'tracked record' object is immutable")
        __delattr__ = __settattr__

        def __init__(self, model=None, id=None):
            super(tracked_record, self).__setattr__('model', model)
            super(tracked_record, self).__setattr__('id', id)

    null_model = tracked_record()

    ct_id = make_content_type_id(model)
    tname = model.__table__.name
    record = tracked_record(model=model, id=ct_id)
    self.model_names[model.__name__] = record
    self.models[model] = record
    self.tables[tname] = record


synched_models = type(
    'synched_models',
    (object,),
    {'tables': dict(),
     'models': dict(),
     'model_names': dict(),
     'ids': dict(),
     'install': install})()

