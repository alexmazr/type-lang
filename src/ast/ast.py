class Program:
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

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
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.left}, "
            f"{self.right})"
        )


class Add(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class Sub(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class Mul(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class Div(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)


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


class String:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.value})"
        )


class Integer:
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
