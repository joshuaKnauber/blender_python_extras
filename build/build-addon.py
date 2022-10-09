from pathlib import Path
import ast
import zipfile
from zipfile import ZipFile
from typing import Callable
from functools import partial


class AddonBuilder:

    def __init__(self, addon_dir: Path, repo_dir: Path = None, build_dir: Path = None):
        if repo_dir is None:
            repo_dir = addon_dir.parent
        if build_dir is None:
            build_dir = repo_dir.joinpath('build')
        self.exclude_dirs: list[Path] = []
        self.build_dir: Path = build_dir
        self.addon_dir: Path = addon_dir
        self.repo_dir: Path = repo_dir

        self.build_name: str = addon_dir.stem

    def _get_addon_init_file(self) -> Path:
        return self.addon_dir.joinpath('__init__.py')

    def _get_git_branch_name(self) -> str:
        file = self.repo_dir.joinpath('.git', 'HEAD')
        with file.open('r') as f:
            content = f.read().splitlines()
        for line in content:
            if line.startswith('ref:'):
                return line.partition('refs/heads/')[2]
        return 'extern'

    def _get_addon_version(self) -> tuple[int, int, int]:
        with self._get_addon_init_file().open('r') as f:
            source_code = ast.parse(f.read())
        return next(ast.literal_eval(n.value) for n in source_code.body if isinstance(n, ast.Assign) and n.targets[0].id == 'bl_info')['version']

    def get_build_file_name(self) -> str:
        version_str = '_'.join([f'{x:02}' for x in self._get_addon_version()])
        return f'{self.build_name}_{self._get_git_branch_name()}_{version_str}'

    def get_target_file(self) -> Path:
        return self.build_dir.joinpath(f'{self.get_build_file_name()}.zip')

    def exclude_path(self, path: Path) -> bool:
        return path.stem == '__pycache__'

    def handle_file_packing(self, path: Path, zip_file: ZipFile) -> None:
        self.pack_file(path, zip_file)

    def to_relative(self, path: Path) -> Path:
        return path.relative_to(self.repo_dir)

    def pack_file(self, path: Path, zip_file: ZipFile, new_name: str = '', new_content: str = None):
        relpath = self.to_relative(path)
        if not new_name == '':
            relpath = relpath.parent.joinpath(f'{new_name}{relpath.suffix}')
        if new_content is None:
            zip_file.write(str(path), arcname=str(relpath))
        else:
            zip_file.writestr(str(relpath), data=new_content)

    def packing_init(self, zip_file: ZipFile) -> None:
        pass

    def packing_finish(self, zip_file: ZipFile) -> None:
        pass

    def build(self):
        with ZipFile(self.get_target_file(), 'w', zipfile.ZIP_DEFLATED) as zf:

            self.packing_init(zf)
            entries = sorted(self.addon_dir.rglob('*'), key=lambda x: x.is_file())
            instructions: list[Callable] = []

            for path in entries:
                if self.exclude_path(path):
                    if path.is_dir():
                        self.exclude_dirs.append(path)
                    continue
                if any(path.is_relative_to(d) for d in self.exclude_dirs):
                    continue
                instructions.append(partial(self.handle_file_packing, path, zf))

            instruction_count = len(instructions)
            for i, instruction in enumerate(instructions):
                instruction()
                print(f'Packaging... [{round(i / instruction_count * 100)}%]', end='\r')
            self.packing_finish(zf)
            print(f'Packaged {len(zf.namelist())} files.')

    def terminal_build(self) -> bool:

        message = 'Build Addon?' if not self.get_target_file().exists() else 'Build and Override Addon?'
        message += f'\nVersion: {self.get_build_file_name()}'

        inp = input(f'{message} (Y/n): ')
        proceed = {'Y': 1, '': 1, 'n': 0}.get(inp, -1)
        if proceed == -1:
            print(f'Command "{inp}" not recognized.')
            proceed = 0
        if proceed == 0:
            return False
        self.build()
        return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('addon_dir', type=str)
    parser.add_argument('build_dir', type=str)
    parser.add_argument('--repo', type=str, required=False, default='.')
    args = parser.parse_args()

    addon_dir = Path(args.addon_dir)
    build_dir = Path(args.build_dir)
    if (repo := args.repo) == '.':
        repo_dir = addon_dir.parent
    else:
        repo_dir = Path(repo)

    builder = AddonBuilder(addon_dir, repo_dir=repo_dir, build_dir=build_dir)

    builder.terminal_build()
    input('Exit...')


if __name__ == "__main__":
    main()
