import yaml
from Spell import *


class DataLoader(yaml.SafeLoader):
    def __init__(self, stream):
        super().__init__(stream)
        super().add_constructor('tag:yaml.org,2002:python/object:Spell.Spell', self.construct_spell)

    def construct_spell(self, loader, node):
        return Spell(**loader.construct_mapping(node))