

class CloudKernelTriggerBase(type):
    '''
    Just a simple Base metaclass to distinguish Cloud Trigger classes
    from all others.  Within the Schedule.py file, there will be an
    isinstance() check!
    '''

    def __subclasscheck__(cls, subclass):
        requirements = getattr(cls, '__triggerattributes__', [])
        for attr in requirements:
            print("ZZZZZ Check it out {}".format(attr))
            if any(attr in sub.__dict__ for sub in subclass.__mro__):
                continue
            return False
        return True
