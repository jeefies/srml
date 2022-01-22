from difflib import SequenceMatcher

class MSG(object):
    "A base object for sending or receiving messages"
    def __eq__(self, ot):
        if (isinstance(ot, MSG)):
            rate = SequenceMatcher.quick_ratio(a=self.raw, b=ot.raw)
            if (rate > 0.9):
                return True
            return False
        raise TypeError("type %s does not support compare with MSG object" % type(ot))
