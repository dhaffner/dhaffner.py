""":class:`transforms` Some high-order functions that use the AST module to
transform and recompile functions.
"""
import ast
from inspect import getsource


__all__ = ['partialize']


def partialize(func):
    source = getsource(func)
    tree = EllipsePartial().visit(ast.parse(source))

    function_def = tree.body[0]
    assert isinstance(function_def, ast.FunctionDef)
    # Change the function definition to remove this partial after it's recompiled.
    function_def = ast.FunctionDef(
        name=function_def.name,
        args=function_def.args,
        body=function_def.body,
        decorator_list=[
            dec for dec in function_def.decorator_list if dec.id != partialize.__name__
        ]
    )

    # Wrap function definition in a module so we can pass it to compile()
    module = ast.Module(body=[function_def])
    ast.fix_missing_locations(module)

    compiled = compile(module, filename='<ast>', mode='exec')
    exec(compiled, globals())
    return globals()[function_def.name]


class EllipsePartial(ast.NodeTransformer):
    def visit_Call(self, node):  # noqa
        ids, args = [], []
        for (i, arg) in enumerate(node.args):
            if not isinstance(arg, ast.Ellipsis):
                args.append(arg)
            else:
                name_id = '_' * (i + 1)
                args.append(ast.Name(id=name_id, ctx=ast.Load()))
                ids.append(name_id)

        if not ids:
            return node

        return ast.Lambda(
            args=ast.arguments(
                args=[ast.arg(id, None, ctx=ast.Param()) for id in ids],
                vararg=None,
                kwarg=None,
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            ),
            body=ast.Call(func=node.func, args=args, keywords=node.keywords)
        )
