from ..ast import ast
from ..logging import logger


log = logger.Log()

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
                self.addToRegistry(statement.typedata.name, statement.base_type, namespace, "Type")
            case ast.FnDef():
                self.addToRegistry(statement.name, statement, namespace, "Function")
            case ast.Declare():
                base_type = self.resolveTypeOf(statement.typedata, namespace)
                expr = self.checkExpression(statement.expr, base_type, namespace)
                self.addToRegistry(statement.name, (expr, base_type), namespace, "Variable")
            case ast.TempDef():
                expr_type = self.resolveTypeOf(statement.expr, namespace)
                expr = self.checkExpression(statement.expr, expr_type, namespace)
                self.addToRegistry(statement.name, (expr, expr_type), namespace, "Temp")
            case _:
                log.warning(f"Statement '{statement}' not added to registry")

    def definitionHandler(self, definition, namespace):
        node = self.registry[definition][namespace]
        match node:
            case ast.FnDef():
                for statement in node.statements:
                    self.statementHandler(statement, namespace + (node.name,))
            case _:
                log.warning(f"definition '{definition}' not checked")

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
                    self.getOrThrowIfNotInNamespace(typename, namespace)
                    self.maybeAddDefinition(statement, namespace)
                else:
                    log.error(f"Type '{typename}' unknown")
            case ast.TempDef():
                self.maybeAddDefinition(statement, namespace)
            case _:
                log.warning(f"Statement '{statement}' not checked")

    def addToRegistry(self, name, value, namespace, typeString):
        if name in self.registry:
            if namespace in self.registry[name]:
                log.error(f"{typeString} '{name}' already defined in '{dot(namespace)}'")
            self.warnIfDefinitionHidesAnother(name, namespace)
            self.registry[name][namespace] = value
        else:
            self.registry[name] = {namespace: value}

    def checkExpression(self, expr, base_type, namespace):
        if isinstance(expr, ast.Literal):
            if isinstance(base_type, ast.Unknown):
                return expr
            base_type.checkValid(expr)
            return expr
        elif isinstance(expr, ast.Ref):
            to_check = self.resolveTypeOf(expr, namespace)
            if isinstance(to_check[1], ast.Unknown):
                base_type.checkValid(self.checkExpression(to_check[0], base_type, namespace))
            elif not to_check[1].compare(base_type):
                log.error(f"Type mismatch in declaration: found '{to_check[1]}', expecting '{base_type}'")
            return to_check[0]
        elif isinstance(expr, ast.BinOp):
            # resolve left and right if either is a ref
            if isinstance(expr.left, ast.Ref):
                expr.left = self.checkExpression(expr.left, base_type, namespace)
            if isinstance(expr.right, ast.Ref):
                expr.right = self.checkExpression(expr.right, base_type, namespace)
            # can only check valid if it's computable
            if isinstance(expr.left, ast.Literal) and isinstance(expr.right, ast.Literal):
                expr = expr.reduceOrThrow()
                base_type.checkValid(expr)
                return expr
            return expr
        elif isinstance(expr, ast.Call):
            # lookup call name in registry
            fndef = self.getOrThrowIfNotInNamespace(expr.name, namespace)
            # check return type matches expected type
            rcontract = self.resolveTypeOf(fndef.rtype, namespace)
            if not rcontract.compare(base_type):
                log.error(f"Call to '{expr.name}' in '{dot(namespace)}' expects '{base_type}', but functions returns '{rcontract}'")
            # match arguments (can only be refs)
            self.typeCheckParameters(expr.params, fndef.args, namespace, expr.name)
        else:
            log.error(f"Type of expression '{expr}' not checked against '{base_type}'")

    def typeCheckParameters(self, parameters, arguments, namespace, callto):
        if len(parameters) != len(arguments):
            log.error(f"Parameter count mismatch in call to '{callto}' in '{dot(namespace)}': found '{len(parameters)}', expecting '{len(arguments)}'")
        for pair in zip(parameters, arguments):
            param_pair = self.resolveTypeOf(pair[0].expr, namespace)
            arg_type = self.resolveTypeOf(pair[1].typedata, namespace)
            if isinstance(param_pair[1], ast.Unknown):
                arg_type.checkValid(param_pair[0])
            elif not param_pair[1].compare(arg_type):
                log.error(f"Type mismatch in call to '{callto}' in '{dot(namespace)}': found '{arg_type}', expecting '{param_pair[1]}'")

    def resolveTypeOf(self, to_resolve, namespace):
        if isinstance(to_resolve, ast.TypeData) or isinstance(to_resolve, ast.Ref):
            if to_resolve.name in self.registry:
                return self.getOrThrowIfNotInNamespace(to_resolve.name, namespace)
            elif isinstance(to_resolve.name, ast.Void):
                return ast.Void()
            log.error(f"Symbol '{to_resolve.name}' not defined")
        elif isinstance(to_resolve, ast.BinOp):
            # resolve left and right if either is a ref
            left = to_resolve.left
            right = to_resolve.right
            if isinstance(to_resolve.left, ast.Ref):
                left = self.resolveTypeOf(to_resolve.left, namespace)
            if isinstance(to_resolve.right, ast.Ref):
                right = self.resolveTypeOf(to_resolve.right, namespace)
            if not isinstance(left, ast.Literal):
                if not isinstance(right, ast.Literal):
                    if not left[1].compare(right[1]):
                        log.error(f"Type mismatch in expression '{to_resolve}' in '{dot(namespace)}': '{to_resolve.left}' and '{to_resolve.right}'")
                return left[1] # left and right are the same or right is a literal
            elif not isinstance(right, ast.Literal):
                return right[1] # left is a literal, right carries type info
            log.error(f"Type of '{to_resolve.left}' and '{to_resolve.right}' unable to be resolved")
        else:
            return ast.Unknown()

    def getOrThrowIfNotInNamespace(self, name, namespace):
        if namespace in self.registry[name]:
            return self.registry[name][namespace]
        for i in range(1, len(namespace)):
            if namespace[:-i] in self.registry[name]:
                return self.registry[name][namespace[:-i]]
        log.error(f"Type '{name}' not visible in '{dot(namespace)}'")

    def warnIfDefinitionHidesAnother(self, name, namespace):
        for i in range(1, len(namespace)):
            if namespace[:-i] in self.registry[name]:
                log.warning(f"Definition '{dot(namespace)}.{name}' hides another definition with the same name in '{dot(namespace[:-1])}'")
                return


def dot(namespace):
    return '.'.join(namespace)
