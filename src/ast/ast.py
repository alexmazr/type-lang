import uuid


class Program:
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

    def flatten(self):
        self.statements = [stmt for statement in self.statements for stmt in statement.flatten()]
        return self

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.statements})"
        )


class ExpressionContainer:
    def flatten(self):
        flatExpr = self.expr.flatten()
        if isinstance(flatExpr, list):
            self.expr = flatExpr.pop()
            return flatExpr + [self]
        elif isinstance(flatExpr, TempDef):
            self.expr = flatExpr.expr
            return [self]
        else:
            self.expr = flatExpr
            return [self]


class Assign(ExpressionContainer):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.expr})"
        )


class Argument:
    def __init__(self, typedata, name, take):
        self.typedata = typedata
        self.name = name
        self.take = take

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"take={self.take}, "
            f"{self.typedata})"
        )


class Parameter(ExpressionContainer):
    def __init__(self, expr, give):
        self.expr = expr
        self.give = give

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr}, "
            f"give={self.give})"
        )


class Call:
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def flatten(self):
        if isinstance(self.name, list):
            self.name = [ref.name for ref in self.name]
        else:
            self.name = self.name.name
        newStatements = []
        flatParams = []
        if self.params is not None:
            for parameter in self.params:
                for param in parameter.flatten():
                    if isinstance(param, Parameter):
                        if not isinstance(param.expr, Ref):
                            temp = TempDef(param.expr)
                            newStatements.append(temp)
                            param.expr = Ref(temp.name)
                            flatParams.append(param)
                        else:
                            flatParams.append(param)
                    else:
                        newStatements.append(param)
        self.params = flatParams
        return newStatements + [self]

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.params})"
        )


class Declare(ExpressionContainer):
    def __init__(self, typedata, name, expr):
        self.typedata = typedata
        self.name = name
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.typedata}, "
            f"{self.expr})"
        )


class New(ExpressionContainer):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class Shared(ExpressionContainer):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class Return(ExpressionContainer):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class Pre(ExpressionContainer):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class Post(ExpressionContainer):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


# todo: remove single ref tempdefs
class TempDef:
    def __init__(self, expr):
        self.expr = expr
        self.name = uuid.uuid4()

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class BinOp:
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def flatten(self):
        self.right = self.right.flatten()
        self.left = self.left.flatten()
        if isinstance(self.left, Literal):
            if isinstance(self.right, Literal):
                return [self.reduceOrThrow()]
        if isinstance(self.left, TempDef):
            if isinstance(self.right, TempDef):
                stmts = [self.left, self.right]
                self.left = Ref(self.left.name)
                self.right = Ref(self.right.name)
                return stmts + [self]
            stmts = [self.left]
            self.left = Ref(self.left.name)
            return stmts + [self]
        if isinstance(self.right, TempDef):
            stmts = [self.right]
            self.right = Ref(self.right.name)
            return stmts + [self]
        return TempDef(self)

    def reduceOrThrow(self):
        if type(self.left) is type(self.right) and type(self.left):
            try:
                return eval(f"{type(self.left).__name__}(self.left.value {self.op} self.right.value)")
            except Exception:
                raise SystemExit(f"Invalid expression: '{self.left.value}' {self.op} '{self.right.value}'")
        else:
            raise SystemExit(f"Operator '{self.op}' undefined for literals {self.left} and {self.right}")

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.left}, "
            f"{self.right})"
        )


class Add(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right, '+')


class Sub(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right, '-')


class Mul(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right, '*')


class Div(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right, '/')


class UnaryOp(ExpressionContainer):
    def __init__(self, expr, op, ctr):
        self.expr = expr
        self.op = op
        self.ctr = ctr

    def flatten(self):
        if isinstance(self.expr, Literal):
            try:
                if isinstance(self.expr, String):
                    raise SystemExit(f"Invalid unary op: '{self.op}' for '{self.expr.value}'")
                return [self.ctr(eval(f"{self.op}{self.expr.value}"))]
            except Exception:
                raise SystemExit(f"Invalid unary op: '{self.op}' for '{self.expr.value}'")
        super().flatten()
        if isinstance(self.expr, Ref):
            return [self]
        temp = TempDef(self.expr)
        self.expr = Ref(temp.name)
        return [temp, self]

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class USub(UnaryOp):
    def __init__(self, expr):
        super().__init__(expr, '-', USub)


class TypeDef:
    def __init__(self, typedata, base_type):
        self.typedata = typedata
        self.base_type = base_type

    def flatten(self):
        return [self]

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.typedata}, "
            f"{self.base_type})"
        )


class Use:
    def __init__(self, locator):
        self.locator = locator

    def flatten(self):
        return [self]

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.locator})"
        )


class RelLocator:
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.path})"
        )


class AbsLocator:
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.path})"
        )


class FnDef:
    def __init__(self, name, annotations, args, give, rtype, statements):
        self.name = name
        self.annotations = annotations
        self.args = args
        self.give = give
        self.rtype = rtype
        self.statements = statements

    def flatten(self):
        self.statements = [stmt for statement in self.statements for stmt in statement.flatten()]
        return [self]

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.annotations}, "
            f"{self.args}, "
            f"{self.give}, "
            f"{self.rtype}, "
            f"{self.statements})"
        )


class Void:
    def compare(self, other):
        return isinstance(other, Void)

    def __repr__(self):
        return (
            f"{type(self).__name__}()"
        )


class TypeData:
    def __init__(self, name, prefix, postfix):
        self.name = name
        self.prefix = prefix
        self.postfix = postfix

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.prefix}, "
            f"{self.postfix})"
        )


class Literal:
    def flatten(self):
        return self


class String(Literal):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.value})"
        )


class Integer(Literal):
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.value})"
        )


class Ref:
    def __init__(self, name):
        self.name = name

    def flatten(self):
        return self

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name})"
        )


class BaseType:
    pass


class Unknown(BaseType):
    def __repr__(self):
        return f"{type(self).__name__}()"


class Unsigned(BaseType):
    def __init__(self, sizeof):
        self.sizeof = sizeof.value
        self.low = 0
        self.high = 2 ** self.sizeof - 1

    def checkValid(self, expr):
        if isinstance(expr, Integer):
            if expr.value < self.low or expr.value > self.high:
                raise SystemExit(f"Integer literal '{expr.value}' out of range for type '{self}'")
        else:
            raise SystemExit(f"'{expr}' is not a valid '{self}'")

    def compare(self, other):
        if isinstance(other, Unsigned):
            return self.sizeof == other.sizeof
        return False

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.sizeof})"
        )
