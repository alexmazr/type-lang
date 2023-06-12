from . import typeregistry
from . import functionregistry
from . import definitions
from ..logging import logger
from ctypes import *


log = logger.Log()

astLine = "========== ast =========="
flatAstLine = "========== flat ast =========="
registryLine = "========== registry =========="


def compile(ast):
    log.debug(f"{astLine}\n{ast}\n{astLine}")
    flatAst = ast.flatten()
    log.debug(f"{flatAstLine}\n{flatAst}\n{flatAstLine}")
    checker = definitions.DefinitionRegistry(flatAst)
    checker.check()
    log.debug(f"{registryLine}\n{checker.registry}\n{registryLine}")
    log.error("Compiler only implemented up to type checking")
    return flatAst
    # build the program type registry
    # program_types = typeregistry.getProgramLevelTypes(ast)
    # build the function registry (should include function scoped type registries)
    # program_functions = functionregistry.getProgramFunctionRegistry(ast, program_types)
    # return (program_functions, program_types)
    # type check  pv
