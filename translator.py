import ast

class PythonToJS:
    def __init__(self):
        self.js_code = []
        self.indentation_level = 0

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
        elif isinstance(node, ast.If):
            self.handle_if(node)
        else:
            self.js_code.append(f"// Unhandled node type: {type(node).__name__}")

    def handle_assign(self, node):
        if len(node.targets) != 1:
            self.js_code.append(self._indent() + "// Multiple assignment not supported")
            return

        target = node.targets[0].id
        value = self.translate_value(node.value)
        self.js_code.append(self._indent() + f"let {target} = {value};")

    def handle_expr(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "print":
            args = []
            for arg in node.value.args:
                if isinstance(arg, ast.JoinedStr):
                    formatted_parts = []
                    for value in arg.values:
                        if isinstance(value, ast.Str):
                            formatted_parts.append(value.s)
                        elif isinstance(value, ast.FormattedValue):
                            formatted_parts.append(f"${{{self.translate_value(value.value)}}}")
                    args.append(f"`{''.join(formatted_parts)}`")
                else:
                    args.append(self.translate_value(arg))
            self.js_code.append(self._indent() + f"console.log({', '.join(args)});")

    def handle_if(self, node):
        test = self.translate_value(node.test)
        self.js_code.append(self._indent() + f"if ({test}) {{")
        self.indentation_level += 1
        for body_node in node.body:
            self.handle_node(body_node)
        self.indentation_level -= 1
        self.js_code.append(self._indent() + "}")
        if node.orelse:
            self.js_code.append(self._indent() + "else {")
            self.indentation_level += 1
            for orelse_node in node.orelse:
                self.handle_node(orelse_node)
            self.indentation_level -= 1
            self.js_code.append(self._indent() + "}")

    def translate_value(self, value):
        if isinstance(value, ast.Constant):
            return repr(value.value)
        elif isinstance(value, ast.Name):
            return value.id
        elif isinstance(value, ast.Compare):
            left = self.translate_value(value.left)
            ops = [self.translate_operator(op) for op in value.ops]
            comparators = [self.translate_value(comp) for comp in value.comparators]
            return f" {ops[0]} ".join([left] + comparators)
        else:
            return "null"

    def translate_operator(self, operator):
        if isinstance(operator, ast.Eq):
            return "=="
        elif isinstance(operator, ast.NotEq):
            return "!="
        elif isinstance(operator, ast.Lt):
            return "<"
        elif isinstance(operator, ast.LtE):
            return "<="
        elif isinstance(operator, ast.Gt):
            return ">"
        elif isinstance(operator, ast.GtE):
            return ">="
        else:
            return "null"

    def _indent(self):
        return "    " * self.indentation_level
