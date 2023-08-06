__all__ = ('exe', 'exe_and_setup')

from pathlib import Path
import shutil
import logging
import subprocess

import PyInstaller.__main__
import jinja2


def exe(
    target, *,
    app_name, icon, dist, build,
    res_dirs: list = None, pyinst_flags: list = None,
    no_clean_dist=False,
):
    if not no_clean_dist:
        clean_dist(dist)

    build_exe(target, app_name, icon, dist, build, res_dirs, pyinst_flags)


def exe_and_setup(
    target, *,
    app_name, icon, app_guid, app_ver, dist, build,
    res_dirs: list = None, pyinst_flags: list = None,
    no_clean_dist=False,
):
    exe(target, app_name=app_name, icon=icon,
        dist=dist, build=build, res_dirs=res_dirs, pyinst_flags=pyinst_flags,
        no_clean_dist=no_clean_dist)

    generate_iss(app_name, icon, app_guid, app_ver, dist)
    build_setup(app_name)


def clean_dist(dist):
    dist_path = Path(dist).resolve()
    logging.info(f'Cleaning "{dist_path}" directory...')

    if not dist_path.exists():
        dist_path.mkdir(parents=True)
        logging.info(
            f'"{dist_path}" directory doesn\'t exist!'
            ' The new one has been created.')
        return

    if not dist_path.is_dir():
        raise FileNotFoundError(
            f'Directory expected, but "{dist_path}" is not!')

    for path in dist_path.iterdir():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

    logging.info(f'"{dist_path}" directory has been cleaned!\n')


def build_exe(
    target, app_name, icon, dist, build,
    res_dirs: list = None, pyinst_flags: list = None,
):
    logging.info(f'Building exe with PyInstaller...')

    args = [
        str(Path(target).resolve()),
        '--name', app_name,
        '--icon', str(Path(icon).resolve()),
        '--distpath', str(Path(dist).resolve()),
        '--workpath', str(Path(build).resolve()),
    ]

    if pyinst_flags:
        args.extend([f'--{it}' for it in pyinst_flags])

    if res_dirs:
        for directory in res_dirs:
            directory_path = Path(directory).resolve()
            if not directory_path.is_dir():
                raise FileNotFoundError(
                    f'Directory expected, but "{directory_path}" is not!')
            args.extend(['--add-data', f'{directory_path};{directory_path.name}'])

    PyInstaller.__main__.run(args)


def generate_iss(app_name, icon, app_guid, app_ver, dist):
    iss_path = Path(f'{app_name}.iss').resolve()
    logging.info(f'Generating "{iss_path}" file...')

    iss_config = {
        'app_name': app_name,
        'app_ico': str(Path(icon).resolve()),
        'app_guid': app_guid,
        'app_ver': app_ver,
        'dist': str(Path(dist).resolve()),
    }

    tmpl_path = Path(__file__).parent / 'templates/iss.tmpl'
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(tmpl_path.parent),
        keep_trailing_newline=True,
        block_start_string='{%%',
        block_end_string='%%}',
        variable_start_string='[{{',
        variable_end_string='}}]',
        comment_start_string='{##',
        comment_end_string='##}',
    )
    template = env.get_template(tmpl_path.name)
    with open(iss_path, 'w') as f:
        f.write(template.render(iss_config))

    logging.info(f'"{iss_path}" file successfully generated!')


def build_setup(app_name):
    """ Inno Setup 6 required (+record in sys PATH).
        https://jrsoftware.org/isdl.php#stable
    """
    logging.info(f'Building setup with Inno Setup...')
    subprocess.run(['iscc', f'{app_name}.iss'], shell=True)
