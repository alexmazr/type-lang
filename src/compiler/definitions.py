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
                base_type = self.resolveBaseType(statement.base_type, namespace)
                self.addToRegistry(statement.typedata.name, base_type, namespace, "Type")
            case ast.FnDef():
                self.addToRegistry(statement.name, statement, namespace, "Function")
            case ast.Declare():
                base_type = self.resolveBaseType(statement.typedata, namespace)
                expr = self.resolveBaseType(statement.expr, namespace)
                expr = self.checkExpression(expr, base_type, namespace)
                self.addToRegistry(statement.name, (expr, base_type), namespace, "Variable")
            case _:
                print(f"WARNING: Statement '{statement}' not added to registry")

    def definitionHandler(self, definition, namespace):
        node = self.registry[definition][namespace]
        match node:
            case ast.FnDef():
                for statement in node.statements:
                    self.statementHandler(statement, namespace + (node.name,))
            case _:
                print(f"WARNING: definition '{definition}' not checked")

    def statementHandler(self, statement, namespace):
        match statement:
            case ast.TypeDef():
                self.maybeAddDefinition(statement, namespace)
            case ast.FnDef():
                self.maybeAddDefinition(statement, namespace)
                self.definitionHandler(statement.name, namespace)
            case ast.Declare():
                typename = statement.typedata.name
                if typename in self.registry:
                    self.throwIfNotInNamespace(typename, namespace)
                    self.maybeAddDefinition(statement, namespace)
                else:
                    raise SystemExit(f"ERROR: Type '{typename}' unknown")
            case _:
                print(f"WARNING: Statement '{statement}' not checked")

    def addToRegistry(self, name, value, namespace, typeString):
        if name in self.registry:
            if namespace in self.registry[name]:
                raise SystemExit(f"ERROR: {typeString} '{name}' already defined in '{dot(namespace)}'")
            self.warnIfDefinitionHidesAnother(name, namespace)
            self.registry[name][namespace] = value
        else:
            self.registry[name] = {namespace: value}

    def checkExpression(self, expr, base_type, namespace):
        if isinstance(expr, ast.Literal):
            base_type.checkValid(expr)
            return expr
        elif isinstance(expr, ast.Ref):
            to_check = self.resolveBaseType(expr, namespace)
            if to_check[1] is not base_type:
                raise SystemExit(f"ERROR: Type mismatch in declaration '{statement}'")
            return to_check[0]
        elif isinstance(expr, ast.BinOp):
            # todo: check if simplifiable, then simplify, then check if type matches
            # if not simplifiable then we cannot know the type range at compile time
            expr.left = self.checkExpression(expr.left, base_type, namespace)
            expr.right = self.checkExpression(expr.right, base_type, namespace)
            return expr

    # def resolveAndThrowIfExpressionTypeMismatch(self, expr, namespace, base_type):
    #     match base_type:
    #         case ast.Unsigned()


    def resolveBaseType(self, base_type, namespace):
        if isinstance(base_type, ast.TypeData) or isinstance(base_type, ast.Ref):
            if base_type.name in self.registry:
                if namespace in self.registry[base_type.name]:
                    return self.registry[base_type.name][namespace]
                for i in range(1, len(namespace)):
                    if namespace[:-i] in self.registry[base_type.name]:
                        return self.registry[base_type.name][namespace[:-i]]
                raise SystemExit(f"ERROR: Symbol '{base_type.name}' not visible in '{dot(namespace)}'")
            raise SystemExit(f"ERROR: Symbol '{base_type.name}' not defined")
        else:
            return base_type

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






