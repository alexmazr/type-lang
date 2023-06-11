from ..ast import ast


class DefinitionRegistry:
    def __init__(self, program):
        self.program = program
        if not isinstance(program, ast.Program):
            raise SystemExit(f"ERROR: The ast root is not a program, is {type(program)}")
        self.registry = {}

    def check(self):
        namespace = (self.program.name, )
        for statement in self.program.statements:
            self.maybeAddDefinition(statement, namespace)
        for definition in self.registry.copy():
            self.definitionHandler(definition, namespace)

    def maybeAddDefinition(self, statement, namespace):
        match statement:
            case ast.TypeDef():
                name = statement.typedata.name
                if name in self.registry:
                    if namespace in self.registry[name]:
                        raise SystemExit(f"ERROR: Type '{name}' already defined in namespace '{dot(namespace)}'")
                    self.warnIfDefinitionHidesAnother(name, namespace)
                    self.registry[name][namespace] = statement.base_type
                else:
                    self.registry[name] = {namespace: statement.base_type}
            case ast.FnDef():
                name = statement.name
                if name in self.registry:
                    if namespace in self.registry[name]:
                        raise SystemExit(f"ERROR: Function '{name}' already defined in namespace '{dot(namespace)}'")
                    self.warnIfDefinitionHidesAnother(name, namespace)
                    self.registry[name][namespace] = statement
                else:
                    self.registry[name] = {namespace: statement}
            case _:
                print(f"WARNING: Statement '{statement}' not added to registry")

    def definitionHandler(self, definition, namespace):
        node = self.registry[definition][namespace]
        match node:
            case ast.FnDef():
                for statement in node.statements:
                    self.statementHandler(statement, namespace + (node.name,))
            case _:
                print(f"WARNING: definition '{definition}' not handled")

    def statementHandler(self, statement, namespace):
        match statement:
            case ast.TypeDef():
                self.maybeAddDefinition(statement, namespace)
            case ast.Declare():
                typename = statement.typedata.name
                if typename in self.registry:
                    self.throwIfNotInNamespace(typename, namespace)
                else:
                    raise SystemExit(f"ERROR: Type '{typename}' unknown")
            case _:
                print(f"WARNING: statement '{statement}' not handled")

    def throwIfNotInNamespace(self, name, namespace):
        if namespace in self.registry[name]:
            return
        for i in range(1, len(namespace)):
            if namespace[:-i] in self.registry[name]:
                return
        raise SystemExit(f"ERROR: Type '{name}' not visible in '{dot(namespace)}'")

    def warnIfDefinitionHidesAnother(self, name, namespace):
        for i in range(1, len(namespace)):
            if namespace[:-i] in self.registry[name]:
                print(f"WARNING: Definition '{dot(namespace)}.{name}' hides another definition with the same name in '{dot(namespace[:-1])}'")
                return

def dot(namespace):
    return '.'.join(namespace)






