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
        elif isinstance(node, ast.For):
            self.handle_for(node)
        elif isinstance(node, ast.While):
            self.handle_while(node)
        elif isinstance(node, ast.FunctionDef):
            self.handle_function_def(node)
        elif isinstance(node, ast.ClassDef):
            self.handle_class_def(node)
        elif isinstance(node, ast.AugAssign):
            self.handle_aug_assign(node)
        elif isinstance(node, ast.Match):
            self.handle_match(node)
        elif isinstance(node, ast.Try):
            self.handle_try(node)
        else:
            self.js_code.append(f"// Unhandled node type: {type(node).__name__}")

    def handle_assign(self, node):
        if len(node.targets) != 1:
            self.js_code.append(self._indent() + "// Multiple assignment not supported")
            return

        target = node.targets[0]
        if isinstance(target, ast.Name):
            target_name = target.id
        elif isinstance(target, ast.Attribute):
            # Handle attribute assignments (e.g., self.name)
            if isinstance(target.value, ast.Name) and target.value.id == "self":
                target_name = f"this.{target.attr}"
            else:
                self.js_code.append(self._indent() + "// Unsupported target type")
                return
        else:
            self.js_code.append(self._indent() + "// Unsupported target type")
            return

        value = self.translate_value(node.value)
        self.js_code.append(self._indent() + f"{target_name} = {value};")

    def handle_aug_assign(self, node):
        target = self.translate_value(node.target)
        op = self.translate_operator(node.op)
        value = self.translate_value(node.value)
        self.js_code.append(self._indent() + f"{target} {op}= {value};")

    def handle_expr(self, node):
        if isinstance(node.value, ast.Call):
            func_name = self.translate_value(node.value.func)
            if func_name == "print":
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
            elif func_name == "input":
                # Translate input() to prompt()
                prompt = self.translate_value(node.value.args[0]) if node.value.args else "''"
                self.js_code.append(self._indent() + f"prompt({prompt});")

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

    def handle_for(self, node):
        target = self.translate_value(node.target)
        iter_value = self.translate_value(node.iter)
        self.js_code.append(self._indent() + f"for (let {target} of {iter_value}) {{")
        self.indentation_level += 1
        for body_node in node.body:
            self.handle_node(body_node)
        self.indentation_level -= 1
        self.js_code.append(self._indent() + "}")

    def handle_while(self, node):
        test = self.translate_value(node.test)
        self.js_code.append(self._indent() + f"while ({test}) {{")
        self.indentation_level += 1
        for body_node in node.body:
            self.handle_node(body_node)
        self.indentation_level -= 1
        self.js_code.append(self._indent() + "}")

    def handle_function_def(self, node):
        func_name = node.name
        args = ", ".join(arg.arg for arg in node.args.args)
        self.js_code.append(self._indent() + f"const {func_name} = ({args}) => {{")
        self.indentation_level += 1
        for body_node in node.body:
            self.handle_node(body_node)
        self.indentation_level -= 1
        self.js_code.append(self._indent() + "}")

    def handle_class_def(self, node):
        class_name = node.name
        self.js_code.append(self._indent() + f"class {class_name} {{")
        self.indentation_level += 1
        for body_node in node.body:
            if isinstance(body_node, ast.FunctionDef):
                self.handle_method_def(body_node)
            else:
                self.handle_node(body_node)
        self.indentation_level -= 1
        self.js_code.append(self._indent() + "}")

    def handle_method_def(self, node):
        method_name = node.name
        args = ", ".join(arg.arg for arg in node.args.args if arg.arg != "self")
        prefix = "constructor" if method_name == "__init__" else method_name
        self.js_code.append(self._indent() + f"{prefix}({args}) {{")
        self.indentation_level += 1
        for body_node in node.body:
            self.handle_node(body_node)
        self.indentation_level -= 1
        self.js_code.append(self._indent() + "}")

    def handle_match(self, node):
        subject = self.translate_value(node.subject)
        self.js_code.append(self._indent() + f"switch ({subject}) {{")
        self.indentation_level += 1

        for case in node.cases:
            # Handle constant patterns via MatchValue
            if isinstance(case.pattern, ast.MatchValue):
                self.js_code.append(self._indent() + f"case {self.translate_value(case.pattern.value)}:")
            # Handle wildcard patterns (`case _`)
            elif isinstance(case.pattern, ast.MatchAs) and case.pattern.name is None:
                self.js_code.append(self._indent() + "default:")
            # Unsupported patterns
            else:
                self.js_code.append(self._indent() + "// Unsupported case pattern")
                continue

            self.indentation_level += 1
            for body_node in case.body:
                self.handle_node(body_node)
            self.js_code.append(self._indent() + "break;")
            self.indentation_level -= 1

        self.indentation_level -= 1
        self.js_code.append(self._indent() + "}")


    def handle_try(self, node):
        self.js_code.append(self._indent() + "try {")
        self.indentation_level += 1
        for body_node in node.body:
            self.handle_node(body_node)
        self.indentation_level -= 1
        self.js_code.append(self._indent() + "}")
        if node.handlers:
            for handler in node.handlers:
                handler_name = handler.name if handler.name else "e"
                handler_type = self.translate_value(handler.type) if handler.type else "Error"
                self.js_code.append(self._indent() + f"catch ({handler_name} /* {handler_type} */) {{")
                self.indentation_level += 1
                for body_node in handler.body:
                    self.handle_node(body_node)
                self.indentation_level -= 1
                self.js_code.append(self._indent() + "}")
        if node.finalbody:
            self.js_code.append(self._indent() + "finally {")
            self.indentation_level += 1
            for body_node in node.finalbody:
                self.handle_node(body_node)
            self.indentation_level -= 1
            self.js_code.append(self._indent() + "}")


    def translate_value(self, value):
        if isinstance(value, ast.Constant):
            return repr(value.value)
        elif isinstance(value, ast.Name):
            return value.id
        elif isinstance(value, ast.Attribute):
            # Handle attributes (e.g., self.name)
            if isinstance(value.value, ast.Name) and value.value.id == "self":
                return f"this.{value.attr}"
            else:
                return f"{self.translate_value(value.value)}.{value.attr}"
        elif isinstance(value, ast.List):
            elements = ", ".join(self.translate_value(el) for el in value.elts)
            return f"[{elements}]"
        elif isinstance(value, ast.Dict):
            keys = [self.translate_value(key) for key in value.keys]
            values = [self.translate_value(val) for val in value.values]
            return "{" + ", ".join(f"{k}: {v}" for k, v in zip(keys, values)) + "}"
        elif isinstance(value, ast.Compare):
            left = self.translate_value(value.left)
            ops = [self.translate_operator(op) for op in value.ops]
            comparators = [self.translate_value(comp) for comp in value.comparators]
            return f" {ops[0]} ".join([left] + comparators)
        elif isinstance(value, ast.BoolOp):
            op = self.translate_operator(value.op)
            values = f" {op} ".join(self.translate_value(v) for v in value.values)
            return values
        elif isinstance(value, ast.Call):
            func_name = self.translate_value(value.func)
            args = ", ".join(self.translate_value(arg) for arg in value.args)
            return f"{func_name}({args})"
        elif isinstance(value, ast.BinOp):
            left = self.translate_value(value.left)
            op = self.translate_operator(value.op)
            right = self.translate_value(value.right)
            return f"{left} {op} {right}"
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
        elif isinstance(operator, ast.Add):
            return "+"
        elif isinstance(operator, ast.Sub):
            return "-"
        elif isinstance(operator, ast.Mult):
            return "*"
        elif isinstance(operator, ast.Div):
            return "/"
        elif isinstance(operator, ast.And):
            return "&&"
        elif isinstance(operator, ast.Or):
            return "||"
        elif isinstance(operator, ast.Not):
            return "!"
        else:
            return "null"

    def _indent(self):
        return "    " * self.indentation_level
