#!/usr/bin/env python3
import argparse
import json
from random import choice
from pathlib import Path
from subprocess import Popen, PIPE
from shutil import copyfile
from sys import exit
import configparser

CONFIG_DIR = Path.home().joinpath('.config', 'theme-change')
THEME_DIR = Path.joinpath(CONFIG_DIR, 'themes')
BG_DIR = Path.joinpath(CONFIG_DIR, 'backgrounds')
SCRIPT_DIR = Path.joinpath(CONFIG_DIR, 'scripts')


def file_exists(path):
    if Path(path).is_file():
        return True
    else:
        return False

def dir_exists(path):
    if Path(path).is_dir():
        return True
    else:
        return False

def apply_theme(theme_file):
    if not file_exists(theme_file):
        print(f'Theme file {theme_file} does not exist!')
        exit(1)
    wal_command = Popen(f'wal -f {theme_file}', shell=True, stdout=PIPE, stderr=PIPE)
    wal_command.wait()
    if args.verbose:
        wal_out, wal_err = wal_command.communicate()
        print(wal_out.decode('utf-8'))
        print(wal_err.decode('utf-8'))
    for script in list(SCRIPT_DIR.glob('*.sh')):
        if args.verbose:
            print(f'========================================================================')
            print(f'Running script {script}')
            print(f'------------------------------------------------------------------------')
        active_script = Popen(f'/bin/sh {script} {theme_file}', shell=True, stdout=PIPE, stderr=PIPE)
        active_script.wait()
        if args.verbose:
            script_out, script_err = active_script.communicate()
            print(script_out.decode('utf-8'))
            if script_err:
                print(f'ERROR: {script_err.decode("utf-8")}')
    print(f'Applied {theme_file.stem}!')


def save_theme(theme_name):
    theme_path = Path.joinpath(THEME_DIR, f'{args.save_theme}.json')
    if file_exists(theme_path):
        print(f'Theme named "{args.save_theme}" already exists at {theme_path}!')
        exit(1)

    with open(Path.home().joinpath('.cache/wal/colors.json')) as f:
        theme_data = json.load(f)
    new_wallpaper_path = Path.joinpath(BG_DIR, Path(theme_data["wallpaper"]).name)
    copyfile(Path(theme_data["wallpaper"]), new_wallpaper_path)
    theme_data["wallpaper"] = f'{new_wallpaper_path}'
    with open(str(theme_path), 'w') as json_file:
        json_file.write(json.dumps(theme_data, indent=4))

    print(f'Saved: {args.save_theme}')
    exit(0)

def main():
    THEME_DIR.mkdir(parents=True, exist_ok=True)
    BG_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    if args.verbose:
        print(f'Using config dir: {CONFIG_DIR}')

    if args.save_theme:
        save_theme(args.save_theme)

    elif args.list_theme:
        print(f'Currently stored themes in {THEME_DIR}:\n')
        [print(f'{item.stem}') for item in list(THEME_DIR.glob('*.json'))]
        exit(0)

    elif args.random_theme:
        try:
            theme_file = choice(
                list(THEME_DIR.glob('*.json')))
        except IndexError:
            print(f'No themes stored in {THEME_DIR}!')
            exit(1)
        if args.verbose:
            print(f'Random Apply: {theme_file}')
        apply_theme(theme_file)

    elif args.apply_theme:
        theme_file = Path.joinpath(THEME_DIR, f'{args.apply_theme}.json')
        if args.verbose:
            print(f'Apply: {args.apply_theme} from {theme_file}')
        apply_theme(theme_file)

    elif args.apply_theme_file:
        theme_file = args.apply_theme_file
        if args.verbose:
            print(f'Apply: {theme_file}')
        apply_theme(theme_file)

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Theme Changer")
    theme = parser.add_mutually_exclusive_group(required=True)
    theme.add_argument('-s', '--save-theme', help='Save current theme')
    theme.add_argument('-a', '--apply-theme', help='Apply stored theme by name')
    theme.add_argument('-f', '--apply-theme-file', help='Apply stored theme file', type=Path)
    theme.add_argument('-r', '--random-theme', help='Apply random stored theme', action="store_true")
    theme.add_argument('-l', '--list-theme', help='List all stored themes', action="store_true")
    parser.add_argument('-v', '--verbose', help='Display additional information', action="store_true")

    args = parser.parse_args()

    main()
