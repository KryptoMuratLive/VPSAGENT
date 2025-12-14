# dependency_mapper.py
import ast
import os

def find_imports_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports

def build_dependency_graph(python_files):
    graph = {}
    for path in python_files:
        module = os.path.splitext(os.path.basename(path))[0]
        imports = find_imports_in_file(path)
        graph[module] = imports
    return graph

if __name__ == "__main__":
    from project_scanner import list_python_files
    root = input("📂 Projektordner angeben (z.B. ../main_orchestrator): ").strip()
    files = list_python_files(root)
    graph = build_dependency_graph(files)
    print("\n📊 Abhängigkeitsgraph:\n")
    for mod, deps in graph.items():
        print(f"{mod} → {', '.join(deps)}")
