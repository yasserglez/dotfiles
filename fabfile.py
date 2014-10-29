import os

from fabric.api import *


def zsh():
    with lcd('zsh'):
        local('sudo apt-get install -y zsh')
        local('chsh -s $(which zsh)')
        if os.path.isdir('prezto'):
            with lcd('prezto'):
                local('git pull')
                local('git submodule update --init --recursive')
        else:
            local('git clone --recursive https://github.com/sorin-ionescu/prezto')
        local('rm -fr ~/.zprezto')
        local('ln -s $PWD/prezto ~/.zprezto')
        local('ln -sf $PWD/prompt_yglezfdez_setup ~/.zprezto/modules/prompt/functions/')
        for dotfile in ('zlogin', 'zlogout', 'zpreztorc', 'zprofile', 'zshenv', 'zshrc'):
            local('rm -f ~/.{0}'.format(dotfile))
            local('ln -s $PWD/{0} ~/.{0}'.format(dotfile))
            
def vim():
    local('sudo apt-get install -y git vim-gnome')
    # ~/.vimrc
    with lcd('vim'):
        local('rm -f ~/.vimrc')
        local('ln -sf "$PWD/vimrc" ~/.vimrc')
    # ~/.vim
    local('rm -rf ~/.vim')
    local('mkdir ~/.vim')
    git_repo = 'https://github.com/gmarik/Vundle.vim'
    git_repo_dir = 'vim/vundle/Vundle.vim'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd('vim'):
        local('ln -sf "$PWD/vundle" ~/.vim/vundle')

def git():
    local('sudo apt-get install -y git')
    # ~/.gitconfig
    with lcd('git'):
        local('rm -f ~/.gitconfig')
        local('ln -sf "$PWD/gitconfig" ~/.gitconfig')
    # ~/.gitignore
    local('rm -f ~/.gitignore')
    git_repo = 'https://github.com/github/gitignore'
    git_repo_dir = 'git/gitignore'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        templates = ('Global/Linux', 'Global/vim', 'Global/Eclipse', 
            'Global/Matlab', 'R', 'Python', 'C', 'C++', 'Java', 'TeX')
        for template in templates:
            local('cat {0}.gitignore >> ~/.gitignore'.format(template))

def solarized(scheme='light'):
    solarized_dircolors(scheme)
    solarized_gnome_terminal(scheme)
    solarized_gedit(scheme)

def solarized_gnome_terminal(scheme):
    git_repo = 'https://github.com/anthony25/gnome-terminal-colors-solarized'
    git_repo_dir = 'solarized/gnome-terminal-colors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        local('sudo apt-get install -y dconf-cli')
        local('./install.sh -s {0} -p Default'.format(scheme))

def solarized_dircolors(scheme):
    git_repo = 'https://github.com/seebi/dircolors-solarized'
    git_repo_dir = 'solarized/dircolors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        local('rm -f ~/.dir_colors')
        local('ln -s "$PWD/dircolors.ansi-{0}" ~/.dir_colors'.format(scheme))

def solarized_gedit(scheme):
    git_repo = 'https://github.com/mattcan/solarized-gedit'
    git_repo_dir = 'solarized/solarized-gedit'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        local('mkdir -p ~/.local/share/gedit/styles')
        local('ln -sf "$PWD/solarized-light.xml" ~/.local/share/gedit/styles/')
        local('ln -sf "$PWD/solarized-dark.xml" ~/.local/share/gedit/styles/')


def _git_pull_or_clone(git_repo, git_repo_dir=None):
    if git_repo_dir is None:
        git_repo_dir = os.path.basename(git_repo)
    if os.path.isdir(git_repo_dir):
        with lcd(git_repo_dir):
            local('git pull')
    else:
        local('git clone {0} {1}'.format(git_repo, git_repo_dir))

