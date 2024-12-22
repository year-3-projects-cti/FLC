from translator import PythonToJS

def main():
    with open("sample.py", "r") as file:
        python_code = file.read()

    translator = PythonToJS()
    js_code = translator.translate(python_code)

    with open("sample.js", "w") as file:
        file.write(js_code)

if __name__ == "__main__":
    main()
