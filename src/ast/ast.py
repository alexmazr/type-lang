class Program:
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

    def flatten(self):
        return [stmt for statement in self.statements for stmt in statement.flatten()]

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.statements})"
        )


class Assign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def flatten(self):
        flatExpr = self.expr.flatten()
        self.expr = flatExpr.pop()
        return flatExpr + [self]

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


class Parameter:
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

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.params})"
        )


class Declare:
    def __init__(self, typename, name, expr):
        self.typename = typename
        self.name = name
        self.expr = expr

    def flatten(self):
        flatExpr = self.expr.flatten()
        self.expr = flatExpr.pop()
        return flatExpr + [self]

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.typename}, "
            f"{self.expr})"
        )


class New:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class Shared:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class Return:
    def __init__(self, expr):
        self.expr = expr

    def flatten(self):
        flatExpr = self.expr.flatten()
        self.expr = flatExpr.pop()
        return flatExpr + [self]

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class Pre:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class Post:
    def __init__(self, expr):
        self.expr = expr

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
        print(f"flattening {self}")
        if isinstance(self.left, Literal):
            print("left is literal")
            if isinstance(self.right, Literal):
                print("right is literal")
                if type(self.left) is type(self.right):
                    print("same literal types")
                    # try:
                    return [eval(f"{type(self.left).__name__}(self.left.value {self.op} self.right.value)")] # compute literal
                    # except Exception:
                    #     raise SystemExit(f"Invalid expression: '{self.left.value}' {self.op} '{self.right.value}'")
                else:
                    raise SystemExit(f"Cannot add two different literal types '{self.left}' and '{self.right}'")
            self.right = self.right.flatten()
        elif isinstance(self.right, Literal):
            self.left = self.left.flatten()
        else:
            self.left = self.left.flatten()
            self.right = self.right.flatten()
        return [self]

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


class UnaryOp:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.expr})"
        )


class USub(UnaryOp):
    def __init__(self, expr):
        super().__init__(expr)


class TypeDef:
    def __init__(self, typedata, base_type):
        self.typedata = typedata 
        self.base_type = base_type

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.typedata}, "
            f"{self.base_type})"
        )


class Use:
    def __init__(self, locator):
        self.locator = locator

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
        return [self]


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
        self.value = value

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.value})"
        )


class Ref:
    def __init__(self, name):
        self.name = name

    def flatten(self):
        return [self]

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name})"
        )


class Unsigned:
    def __init__(self, sizeof):
        self.sizeof = sizeof

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.sizeof})"
        )
