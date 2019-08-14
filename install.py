#!/usr/bin/env python

import os
import sys
import shutil
import argparse


HOME_DIR = os.path.expanduser('~')
DOTFILES_DIR = os.path.abspath(os.path.dirname(__file__))


def _remove_with_confirmation(path):
    os.system('rm -fr{} {}'.format('I' if sys.platform == 'linux' else 'i', path))


def install_emacs():
    src_dir = f'{DOTFILES_DIR}/emacs'
    dest_dir = f'{HOME_DIR}/.emacs.d'
    _remove_with_confirmation(dest_dir)
    os.mkdir(dest_dir)
    for name in os.listdir(src_dir):
        print(f'installing {dest_dir}/{name}')
        os.symlink(f'{src_dir}/{name}', f'{dest_dir}/{name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Install the configuration files.')
    applications = {k[8:]: v for k, v in locals().items() if k.startswith('install_')}
    parser.add_argument('application', help='application name', choices=sorted(applications.keys()))
    args = parser.parse_args()
    applications[args.application]()
