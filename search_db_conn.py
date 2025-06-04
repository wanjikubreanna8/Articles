import os
import ast
import importlib.util
import sys

def get_connection(root_dir="."):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(".py"):
                continue

            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=file_path)
            except SyntaxError:
                continue

            for node in tree.body:
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                    call = node.value
                    if (
                        isinstance(call.func, ast.Attribute)
                        and call.func.attr == "connect"
                        and isinstance(call.func.value, ast.Name)
                        and call.func.value.id == "sqlite3"
                    ):
                        var_name = node.targets[0].id
                        # Dynamically import the module
                        spec = importlib.util.spec_from_file_location("target_module", file_path)
                        module = importlib.util.module_from_spec(spec)
                        sys.modules["target_module"] = module
                        spec.loader.exec_module(module)

                        conn_obj = getattr(module, var_name, None)
                        if conn_obj:
                            print(f"✅ Loaded: {var_name} from {file_path}")
                            return conn_obj

    print("❌ No sqlite3 connection variable found.")
    return None

# Run the search
# if __name__ == "__main__":
#     find_sqlite_connection_var()