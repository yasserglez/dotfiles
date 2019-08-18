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


def _apt_get_install(*packages):
    for pkg in packages:
        os.system(f'sudo apt-get install --yes {pkg}')


def _rm_confirm(path):
    if os.path.exists(path):
        os.system('rm -ri {}'.format(path))


def _git_pull_or_clone(git_repo, git_repo_dir):
    if os.path.isdir(git_repo_dir):
        with _chdir(git_repo_dir):
            os.system('git pull')
            os.system('git submodule update --init --recursive')
    else:
        os.system('git clone --recursive {} {}'
                  .format(git_repo, git_repo_dir))


def install_emacs():
    src_dir = f'{DOTFILES_DIR}/emacs'
    dest_dir = f'{HOME_DIR}/.emacs.d'
    _rm_confirm(dest_dir)
    os.mkdir(dest_dir)
    for name in os.listdir(src_dir):
        os.symlink(f'{src_dir}/{name}', f'{dest_dir}/{name}')


def install_vim():
    _apt_get_install('git', 'vim-nox')

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
    _apt_get_install(
        'build-essential',
        'curl',
        'libffi-dev',
        'libsqlite3-dev',
        'libssl-dev',
        'python',
        'python-dev',
        'python-pip')
    os.system('curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash')


def install_R():
    _apt_get_install('r-base', 'r-base-dev')

    os.system('mkdir -p ~/.local/lib/R/library')

    src_file = f'{DOTFILES_DIR}/R/Rprofile'
    dest_file = f'{HOME_DIR}/.Rprofile'
    _rm_confirm(dest_file)
    os.symlink(src_file, dest_file)


def install_git():
    _apt_get_install('git')

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
            'Global/Linux',
            'Global/Vim',
            'Global/Emacs',
            'Python',
            'R',
            'C',
            'C++',
            'Java',
            'Scala',
            'TeX',
        ]
        for template in templates:
            os.system(f'cat {template}.gitignore >> ~/.gitignore')


def install_zsh():
    _apt_get_install('zsh')
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

def install_terminal():
    _apt_get_install('gnome-terminal', 'dconf-cli')
    git_repo = 'https://github.com/anthony25/gnome-terminal-colors-solarized'
    git_repo_dir = f'{DOTFILES_DIR}/solarized/gnome-terminal-colors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with _chdir(git_repo_dir):
        os.system('./install.sh -s dark -p Default')


def install_dircolos():
    _apt_get_install('coreutils')
    git_repo = 'https://github.com/seebi/dircolors-solarized'
    git_repo_dir = f'{DOTFILES_DIR}/solarized/dircolors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    _rm_confirm(f'{HOME_DIR}/.dir_colors')
    os.symlink(f'{git_repo_dir}/dircolors.ansi-dark',
               f'{HOME_DIR}/.dir_colors')

def install_bin():
    local_bin = f'{HOME_DIR}/.local/bin'
    os.system('mkdir -p {}'.format(local_bin))
    for bin_file in os.listdir('bin'):
        bin_path = os.path.join(local_bin, bin_file)
        _rm_confirm(bin_path)
        os.symlink(f'{DOTFILES_DIR}/bin/{bin_file}', bin_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Install the configuration files.')
    applications = {k[8:]: v for k, v in locals().items()
                    if k.startswith('install_')}
    parser.add_argument('application', help='application name',
                        choices=sorted(applications.keys()))
    args = parser.parse_args()
    applications[args.application]()
