import os
import yaml

from jinja2 import Environment, FileSystemLoader
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

# static values
dconf = "[dconf](https://wiki.gnome.org/Projects/dconf)"
test_env_path = "`extensions/molecule/gnome_setup_test`"
profile_picture_path = "`~/Documents/vagrant`"

# dynamic values
data_files = [
    {
        "path": "../extensions/molecule/gnome_setup_test/molecule.yml",
        "key": "platforms",
    },
    {
        "path": "./defaults/main/extensions.yml",
        "key": "gnome_extensions",
    },
    {
        "path": "./defaults/main/themes.yml",
        "key": "gnome_themes",
    },
    {
        "path": "../extensions/molecule/gnome_setup_test/converge.yml",
        "key": 0,
    },
    {
        "path": "./vars/main.yml",
        "key": "dependencies",
    }
]

def get_yaml_data(data_files: dict) -> list:
    yaml_content_list = []
    for path in data_files:
        with open(path["path"], "r") as file:
            yaml_content = yaml.load(file, SafeLoader)
            yaml_content_list.append(yaml_content[path["key"]])

    return yaml_content_list

yaml_output = get_yaml_data(data_files)

vm_list = [distro["name"] for distro in yaml_output[0]]
extension_list = yaml_output[1]
theme_list = yaml_output[2]
role_present = f"---\n\n{yaml.dump(yaml_output[3], Dumper=yaml.CSafeDumper, indent=2, sort_keys=False)}\n..."
global_dependencies = yaml_output[4]

print(vm_list)
print(extension_list)
print(theme_list)
print(role_present)
print(global_dependencies)

# file tree
def generate_tree_visualization(base_path, prefix=""):
    tree_visualization = []
    items = sorted(os.listdir(base_path))
    pointers = ['┣ ' for _ in items[:-1]] + ['┗ ']

    for pointer, item in zip(pointers, items):
        path = os.path.join(base_path, item)
        if os.path.isdir(path):
            tree_visualization.append(f"{prefix}{pointer}📂 {item}")
            extension = '┃ ' if pointer == '┣ ' else '  '
            tree_visualization.extend(generate_tree_visualization(path, prefix + extension))
        else:
            tree_visualization.append(f"{prefix}{pointer}📜 {item}")
    
    return tree_visualization

root_dir = "/home/dev_test/setup_automation/gnome_setup"
tree_visualization = generate_tree_visualization(root_dir)
tree_text = "\n ".join(tree_visualization)
dir_structure = f"📦 {os.path.basename(root_dir)}\n {os.path.basename(tree_text)}\n"

# output file
environment = Environment(loader=FileSystemLoader("templates/"))
results_filename = "readme_test.md"
results_template = environment.get_template("README_template.j2")
context = {
    "dconf": dconf,
    "vm_list": vm_list,
    "dir_structure": dir_structure,
    "profile_picture_path": profile_picture_path,
    "test_env_path": test_env_path,
    "extension_list": extension_list,
    "theme_list": theme_list,
    "role_present": role_present,
    "global_dependencies": global_dependencies
}

with open(results_filename, mode="w", encoding="utf-8") as message:
    message.write(results_template.render(context))
    print(f"wrote {results_filename}")
