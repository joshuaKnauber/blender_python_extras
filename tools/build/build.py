import os
import shutil

def build_addon(dirname):
    """ Builds the addon to the given directory """
    addon_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    build_dir = os.path.join(addon_dir, dirname)
    delete_current_build(build_dir)
    create_build_dir(build_dir)
    create_addon_build(addon_dir, build_dir)
    write_gitignore(os.path.join(addon_dir, ".gitignore"), dirname)

def delete_current_build(build_dir):
    """ Deletes the current build directory """
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

def create_build_dir(build_dir):
    """ Creates the build directory """
    os.makedirs(build_dir)

def write_gitignore(gitignore_path, dirname):
    """ Writes the gitignore file """
    if os.path.exists(gitignore_path):
        lines = []
        with open(gitignore_path, "r") as f:
            lines = list(map(lambda line: line.strip(), f.readlines()))
        if not "" in lines:
            lines.append(f"\n/{dirname}")
        with open(gitignore_path, "w") as f:
            f.seek(0)
            f.write("\n".join(lines))
            f.truncate()

def create_addon_build(addon_dir, build_dir):
    """ Creates the addon build """
    pass