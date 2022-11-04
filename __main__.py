import subprocess
import sys
import importlib.util

def install_required_packages():
    required_packages = ["click", "inquirer", "colorama"]
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == '__main__':
    install_required_packages()
    from cli.cli import cli
    cli()