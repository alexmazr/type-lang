from ..ast import ast
from . import builtinfn


class ArgumentContract:
    def __init__(self, take, typename, prefix, postfix):
        self.take = take
        self.typename = typename
        self.prefix = prefix
        self.postfix = postfix

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"take={self.take}, "
            f"{self.typename}, "
            f"{self.prefix}, "
            f"{self.postfix})"
        )


class ReturnContract:
    def __init__(self, give, typename, prefix, postfix):
        self.give = give
        self.typename = typename
        self.prefix = prefix
        self.postfix = postfix

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"give={self.give}, "
            f"{self.typename}, "
            f"{self.prefix}, "
            f"{self.postfix})"
        )


class FunctionContract:
    def __init__(self, argumentContracts, returnContract):
        self.argumentContracts = argumentContracts
        self.returnContract = returnContract

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.argumentContracts}, "
            f"{self.returnContract})"
        )


class RemoteFunction:
    def __init__(self, remoteReference):
        self.remoteReference = remoteReference

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.remoteReference})"
        )


class NativeFunction:
    def __init__(self, function):
        self.function = function

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.function})"
        )


class Function:
    def __init__(self, contract, body):
        self.contract = contract
        self.body = body

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.contract}, "
            f"{self.body})"
        )


def getProgramFunctionRegistry(program, type_registry):
    function_registry = {
        'print': Function(FunctionContract([ArgumentContract(False, 'String', None, None)], ReturnContract(False, 'void', None, None)), RemoteFunction(builtinfn.remotePrint)),
        'input': Function(FunctionContract([ArgumentContract(False, 'String', None, None)], ReturnContract(True, 'String', None, None)), RemoteFunction(builtinfn.remoteInput))
    }
    for statement in program.statements:
        if isinstance(statement, ast.FnDef):
            function_registry = addFunctionToRegistry(statement, function_registry)
    if 'main' not in function_registry:
        raise SystemExit("Function 'main' not defined")
    return function_registry


def addFunctionToRegistry(function, function_registry):
    name = function.name
    give = function.give
    rtype = function.rtype
    argContracts = [ArgumentContract(arg.take, arg.typedata.name, arg.typedata.prefix, arg.typedata.postfix) for arg in function.args]
    retContract = ReturnContract(give, rtype.name, rtype.prefix, rtype.postfix)
    if name in function_registry:
        raise SystemExit(f"Function '{name}' already defined, overloading not supported yet")
    function_registry[name] = Function(FunctionContract(argContracts, retContract), NativeFunction(function))
    return function_registry




