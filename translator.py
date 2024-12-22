import ast

class PythonToJS:
    def __init__(self):
        self.js_code = []

    def translate(self, python_code):
        parsed_ast = ast.parse(python_code)
        for node in parsed_ast.body:
            self.handle_node(node)
        return "\n".join(self.js_code)

    def handle_node(self, node):
        if isinstance(node, ast.Assign):
            self.handle_assign(node)
        elif isinstance(node, ast.Expr):
            self.handle_expr(node)
        else:
            self.js_code.append(f"// Unhandled node type: {type(node).__name__}")

    def handle_assign(self, node):
        if len(node.targets) != 1:
            self.js_code.append("// Multiple assignment not supported")
            return

        target = node.targets[0].id
        value = self.translate_value(node.value)
        self.js_code.append(f"let {target} = {value};")

    def handle_expr(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "print":
            args = ", ".join(self.translate_value(arg) for arg in node.value.args)
            self.js_code.append(f"console.log({args});")

    def translate_value(self, value):
        if isinstance(value, ast.Constant):
            return repr(value.value)
        elif isinstance(value, ast.Name):
            return value.id
        else:
            return "null"

    def translate_operator(self, operator):
        pass
