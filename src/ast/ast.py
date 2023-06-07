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


class Argument:
    def __init__(self, typename, name):
        self.typename = typename
        self.name = name

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.typename}, "
            f"{self.name})"
        )


class Declare:
    def __init__(self, typename, name, expr):
        self.typename = typename
        self.name = name
        self.expr = expr

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.typename}, "
            f"{self.name}, "
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
    def __init__(self, name, base_type):
        self.name = name
        self.base_type = base_type

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
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
    def __init__(self, name, args, rtype, statements):
        self.name = name
        self.args = args
        self.rtype = rtype
        self.statements = statements

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name}, "
            f"{self.args}, "
            f"{self.rtype}, "
            f"{self.statements})"
        )


class Void:
    def __repr__(self):
        return (
            f"{type(self).__name__}()"
        )


class TypeName:
    def __init__(self, name, optional, error):
        self.name = name
        self.optional = optional
        self.error = error

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.optional}, "
            f"{self.error}, "
            f"{self.name})"
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
