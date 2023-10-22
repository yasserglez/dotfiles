#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
from contextlib import contextmanager


HOME_DIR = os.path.expanduser('~')
DOTFILES_DIR = os.path.abspath(os.path.dirname(__file__))


@contextmanager
def _chdir(dir_path):
    old_dir_path = os.getcwd()
    os.chdir(dir_path)
    yield
    os.chdir(dir_path)


def _brew_install(*packages):
    for pkg in packages:
        os.system(f'brew install {pkg}')

def _brew_install_cask(*packages):
    for pkg in packages:
        os.system(f'brew install --cask {pkg}')


def _rm_confirm(path):
    if os.path.exists(path):
        os.system('rm -rI {}'.format(path))


def _git_pull_or_clone(git_repo, git_repo_dir):
    if os.path.isdir(git_repo_dir):
        with _chdir(git_repo_dir):
            os.system('git pull')
            os.system('git submodule update --init --recursive')
    else:
        os.system('git clone --recursive {} {}'
                  .format(git_repo, git_repo_dir))


def install_emacs():
    _brew_install_cask('emacs')
    src_dir = f'{DOTFILES_DIR}/emacs'
    dest_dir = f'{HOME_DIR}/.emacs.d'
    _rm_confirm(dest_dir)
    os.mkdir(dest_dir)
    for name in os.listdir(src_dir):
        os.symlink(f'{src_dir}/{name}', f'{dest_dir}/{name}')


def install_vim():
    _brew_install('git', 'vimx')

    src_file = f'{DOTFILES_DIR}/vim/vimrc'
    dest_file = f'{HOME_DIR}/.vimrc'
    _rm_confirm(dest_file)
    os.symlink(src_file, dest_file)

    dest_dir = f'{HOME_DIR}/.vim'
    _rm_confirm(dest_dir)
    os.system(f'mkdir {dest_dir}')
    git_repo = 'https://github.com/gmarik/Vundle.vim'
    git_repo_dir = f'{DOTFILES_DIR}/vim/vundle/Vundle.vim'
    _git_pull_or_clone(git_repo, git_repo_dir)
    os.symlink(f'{DOTFILES_DIR}/vim/vundle/', f'{dest_dir}/vundle')


def install_python():
    _brew_install('pyenv')


def install_git():
    _brew_install('git')

    src_file = f'{DOTFILES_DIR}/git/gitconfig'
    dest_file = f'{HOME_DIR}/.gitconfig'
    _rm_confirm(dest_file)
    os.symlink(src_file, dest_file)

    dest_file = f'{HOME_DIR}/.gitignore'
    _rm_confirm(dest_file)
    git_repo = 'https://github.com/github/gitignore'
    git_repo_dir = f'{DOTFILES_DIR}/git/gitignore'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with _chdir(git_repo_dir):
        templates = [
            'Global/macOS',
            'Global/Vim',
            'Global/Emacs',
            'Python',
            'TeX',
        ]
        for template in templates:
            os.system(f'cat {template}.gitignore >> ~/.gitignore')


def install_zsh():
    _brew_install('zsh')
    os.system('chsh -s /usr/bin/zsh')

    git_repo = 'https://github.com/sorin-ionescu/prezto'
    git_repo_dir = f'{DOTFILES_DIR}/zsh/prezto'
    _git_pull_or_clone(git_repo, git_repo_dir)

    _rm_confirm(f'{HOME_DIR}/.zprezto')
    os.symlink(f'{DOTFILES_DIR}/zsh/prezto', f'{HOME_DIR}/.zprezto')

    dest_file = f'{HOME_DIR}/.zprezto/modules/prompt/functions/prompt_yasserglez_setup'
    _rm_confirm(dest_file)
    os.symlink(f'{DOTFILES_DIR}/zsh/prompt_yasserglez_setup', dest_file)

    for dotfile in ('zlogin', 'zlogout', 'zpreztorc', 'zprofile', 'profile', 'zshenv', 'zshrc'):
        src_file = f'{DOTFILES_DIR}/zsh/{dotfile}'
        dest_file = f'{HOME_DIR}/.{dotfile}'
        _rm_confirm(dest_file)
        os.symlink(src_file, dest_file)

def install_dircolors():
    _brew_install('coreutils')
    git_repo = 'https://github.com/seebi/dircolors-solarized'
    git_repo_dir = f'{DOTFILES_DIR}/solarized/dircolors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    _rm_confirm(f'{HOME_DIR}/.dircolors')
    os.symlink(f'{git_repo_dir}/dircolors.ansi-dark',
               f'{HOME_DIR}/.dircolors')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Install the configuration files.')
    applications = {k[8:]: v for k, v in locals().items()
                    if k.startswith('install_')}
    parser.add_argument('application', help='application name',
                        choices=sorted(applications.keys()))
    args = parser.parse_args()
    applications[args.application]()
