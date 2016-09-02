import ast

from importlib import import_module
from importlib.machinery import PathFinder, SourceFileLoader
import sys


transformers = []


def transform(tree, transfomers):
    """Apply transformations to ast."""
    for module_name in transformers:
        module = import_module('.{}'.format(module_name), 'dhaffner.transformers')
        tree = module.transformer.visit(tree)

    return tree


class Loader(SourceFileLoader):
    def source_to_code(self, data, path, *, _optimize=-1):
        tree = ast.parse(data)
        tree = transform(tree, transformers)
        return compile(tree, path, 'exec', dont_inherit=True, optimize=_optimize)


class Finder(PathFinder):
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        spec = super(Finder, cls).find_spec(fullname, path, target)
        if spec is None:
            return None

        spec.loader = Loader(spec.loader.name, spec.loader.path)
        return spec


def transformer(Transformer):  # noqa
    if Transformer not in transformers:
        transformers.append(Transformer)
    if Finder not in sys.meta_path:
        sys.meta_path.insert(0, Finder)

    # Enable use as a decorator
    return Transformer
