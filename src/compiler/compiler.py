from . import typeregistry
from . import functionregistry


def compile(ast):
    # build the program type registry
    program_types = typeregistry.getProgramLevelTypes(ast)
    # build the function registry (should include function scoped type registries)
    program_functions = functionregistry.getProgramFunctionRegistry(ast, program_types)
    return (program_functions, program_types)
    # type check  pv
