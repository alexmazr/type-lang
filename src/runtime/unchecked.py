from ..ast import ast
from ..compiler import functionregistry


def run(function_registry, type_registry):
    executeFunction(function_registry['main'].body.function, function_registry, type_registry)


def executeFunction(function, function_registry, type_registry):
    local_variable_registry = {}
    for statement in function.statements:
        match statement:
            case ast.Declare():
                local_variable_registry[statement.name] = resolveExpression(statement.expr, local_variable_registry, function_registry, type_registry)                
            case ast.Call():
                verifyAndMaybeExecuteCall(statement, function_registry, type_registry)
    print(f"terminating... {local_variable_registry}")


def resolveExpression(expr, local_variable_registry, function_registry, type_registry):
    match expr:
        case ast.Call():
            return verifyAndMaybeExecuteCall(expr, function_registry, type_registry)
        case _:
            raise SystemExit(f"expression {expr} not implemented yet")


def verifyAndMaybeExecuteCall(call, function_registry, type_registry):
    if call.name.name not in function_registry:
        raise SystemExit(f"Function {call.name.name} is undefined")
    function = function_registry[call.name.name]
    match function.body:
        case functionregistry.NativeFunction():
            print("calling a native function not implemented yet")
        case functionregistry.RemoteFunction():
            return function.body.remoteReference(call.params)




