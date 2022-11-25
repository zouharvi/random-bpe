from .base import BaseBPE

class AntiStandardBPE(BaseBPE):
    def __init__(self):
        pass

    def choose_pair_to_merge(self, pairs):
        return min(pairs, key=pairs.get)