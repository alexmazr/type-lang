from ..ast import ast
from ctypes import *


def getProgramLevelTypes(program):
    type_registry = {}
    for statement in program.statements:
        if isinstance(statement, ast.TypeDef):
            typedata = statement.typedata
            if typedata.prefix is not None:
                raise SystemExit(f"Illegal modifier '{typedata.prefix}' in type definition for '{typedata.name}'")
            if typedata.postfix is not None:
                raise SystemExit(f"Illegal modifier '{typedata.postfix}' in type definition for '{typedata.name}'")
            if typedata.name in type_registry:
                raise SystemExit(f"Type '{typedata.name}' already defined in namespace")
            type_registry[typedata.name] = resolveBaseType(statement.base_type)
    return type_registry


# returns a method reference to a c_type constructor
def resolveBaseType(base_type):
    if isinstance(base_type, ast.Unsigned):
        if isinstance(base_type.sizeof, ast.Integer):
            match base_type.sizeof.value:
                case '8':
                    return c_uint8
                case '16':
                    return c_uint16
                case '32':
                    return c_uint32
                case '64':
                    return c_uint64
                case _:
                    raise SystemExit(f"Unsupported unsigned integer size '{base_type.sizeof.value}'")
        else:
            raise SystemExit(f"Unsupported unsigned sizeof type '{base_type.sizeof}'")
    else:
        raise SystemExit(f"Unknown base type '{base_type}'")

