import argparse
import logging

from .pyappbundler import exe, exe_and_setup


parser = argparse.ArgumentParser(
    prog='pyappbundler',
    description="""Automate bundle a Python application and all its
        dependencies into a single package with PyInstaller
        (https://pyinstaller.org/en/stable). And then (for Windows), put it all into
        a setup file with Inno Setup (https://jrsoftware.org/isdl.php#stable).""",
)

parser.add_argument(
    '-t', '--target', required=True, help='target python script')
parser.add_argument(
    '-a', '--app-name', required=True, help='application name')
parser.add_argument(
    '-i', '--icon', required=True, help='application icon')
parser.add_argument(
    '-g', '--app-guid', required=True, help='application GUID')
parser.add_argument(
    '-v', '--app-ver', required=True, help='application version')

parser.add_argument(
    '-r', '--res-dir', action="extend", nargs=1,
    help="""Directory with additional files to be added to the executable.
        Multiple definitions are allowed.""")
parser.add_argument(
    '-f', '--pyinst-flag', action="extend", nargs=1,
    help=f"""FLAG-argument (without "--" prefix) for PyInstaller.
        Multiple definitions are allowed.
        Example: "... -f windowed -f clean ..." will pass "--windowed"
        and "--clean" flags to PyInstaller during application bundling.""")

parser.add_argument(
    '--dist-dir', default='dist',
    help='Distribution directory path. "dist" byte default.')
parser.add_argument(
    '--build-dir', default='build',
    help='Where PyInstaller put all the temporary work files. "build" by default.')
parser.add_argument(
    '--no-clean-dist', action='store_true',
    help='cancel cleaning dist directory before building')
parser.add_argument(
    '--no-setup', action='store_true',
    help='build exe without setup-file')

args = parser.parse_args()

#
logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO,
)

#
if args.no_setup:
    exe(
        args.target,
        app_name=args.app_name, icon=args.icon,
        dist=args.dist_dir, build=args.build_dir,
        res_dirs=args.res_dir, pyinst_flags=args.pyinst_flag,
        no_clean_dist=args.no_clean_dist,
    )
else:
    exe_and_setup(
        args.target,
        app_name=args.app_name, icon=args.icon,
        app_guid=args.app_guid, app_ver=args.app_ver,
        dist=args.dist_dir, build=args.build_dir,
        res_dirs=args.res_dir, pyinst_flags=args.pyinst_flag,
        no_clean_dist=args.no_clean_dist,
    )
