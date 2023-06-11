from . import typeregistry
from . import functionregistry
from . import definitions


def compile(ast):
    print("========== ast ==========")
    print(ast)
    print("========== ast ==========")
    flatAst = ast.flatten()
    print("========== flat ast ==========")
    print(flatAst)
    print("========== flat ast ==========")
    checker = definitions.DefinitionRegistry(flatAst)
    checker.check()
    print("========== registry ==========")
    print(checker.registry)
    print("========== registry ==========")
    return flatAst
    # build the program type registry
    # program_types = typeregistry.getProgramLevelTypes(ast)
    # build the function registry (should include function scoped type registries)
    # program_functions = functionregistry.getProgramFunctionRegistry(ast, program_types)
    # return (program_functions, program_types)
    # type check  pv
