import os

from fabric.api import lcd, local
from fabric.contrib.console import confirm

def emacs():
    _apt_get_install('emacs24')
    if _can_overwrite('~/.emacs.d'):
        local('rm -rf ~/.emacs.d')
        local('mkdir ~/.emacs.d')
        with lcd('emacs'):
            local('ln -s $PWD/init.el ~/.emacs.d/init.el')
            local('ln -s $PWD/config.org ~/.emacs.d/config.org')

def vim():
    _apt_get_install('git', 'vim-nox')
    if _can_overwrite('~/.vimrc'):
        with lcd('vim'):
            local('rm -f ~/.vimrc')
            local('ln -sf "$PWD/vimrc" ~/.vimrc')
    if _can_overwrite('~/.vim'):
        local('rm -rf ~/.vim')
        local('mkdir ~/.vim')
        git_repo = 'https://github.com/gmarik/Vundle.vim'
        git_repo_dir = 'vim/vundle/Vundle.vim'
        _git_pull_or_clone(git_repo, git_repo_dir)
        with lcd('vim'):
            local('ln -sf $PWD/vundle ~/.vim/vundle')

def git():
    _apt_get_install('git')
    if _can_overwrite('~/.gitconfig'):
        with lcd('git'):
            local('rm -f ~/.gitconfig')
            local('ln -sf $PWD/gitconfig ~/.gitconfig')
    if _can_overwrite('~/.gitignore'):
        local('rm -f ~/.gitignore')
        git_repo = 'https://github.com/github/gitignore'
        git_repo_dir = 'git/gitignore'
        _git_pull_or_clone(git_repo, git_repo_dir)
        with lcd(git_repo_dir):
            templates = ('Global/Linux', 'Global/vim', 'Global/Emacs',
                'Global/Eclipse', 'Global/Matlab', 'R', 'Python', 'C',
                'C++', 'Java', 'TeX')
            for template in templates:
                local('cat {0}.gitignore >> ~/.gitignore'.format(template))

def zsh():
    _apt_get_install('zsh')
    local('chsh -s /usr/bin/zsh')
    git_repo = 'https://github.com/sorin-ionescu/prezto'
    git_repo_dir = 'zsh/prezto'
    _git_pull_or_clone(git_repo, git_repo_dir)
    if _can_overwrite('~/.zprezto'):
        with lcd('zsh'):
            local('rm -fr ~/.zprezto')
            local('ln -s $PWD/prezto ~/.zprezto')
            local('ln -s $PWD/prompt_yglezfdez_setup ~/.zprezto/modules/prompt/functions/')
    for dotfile in ('zlogin', 'zlogout', 'zpreztorc', 'zprofile', 'zshenv', 'zshrc'):
        if _can_overwrite('~/.{0}'.format(dotfile)):
            local('rm -f ~/.{0}'.format(dotfile))
            local('ln -s $PWD/{0} ~/.{0}'.format(dotfile))

def solarized(scheme='dark'):
    solarized_dircolors(scheme)
    solarized_gnome_terminal(scheme)
    solarized_gedit(scheme)

def solarized_gnome_terminal(scheme):
    git_repo = 'https://github.com/anthony25/gnome-terminal-colors-solarized'
    git_repo_dir = 'solarized/gnome-terminal-colors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        _apt_get_install('dconf-cli')
        local('./install.sh -s {0} -p Default'.format(scheme))

def solarized_dircolors(scheme):
    git_repo = 'https://github.com/seebi/dircolors-solarized'
    git_repo_dir = 'solarized/dircolors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    if _can_overwrite('~/.dir_colors'):
        with lcd(git_repo_dir):
            local('rm -f ~/.dir_colors')
            local('ln -s $PWD/dircolors.ansi-{0} ~/.dir_colors'.format(scheme))

def solarized_gedit(scheme):
    git_repo = 'https://github.com/mattcan/solarized-gedit'
    git_repo_dir = 'solarized/solarized-gedit'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        local('mkdir -p ~/.local/share/gedit/styles')
        local('ln -sf $PWD/solarized-light.xml ~/.local/share/gedit/styles/')
        local('ln -sf $PWD/solarized-dark.xml ~/.local/share/gedit/styles/')

def _can_overwrite(file_or_dir):
    file_or_dir = os.path.expanduser(file_or_dir)
    msg = 'Overwrite {0}?'.format(file_or_dir)
    return not os.path.exists(file_or_dir) or confirm(msg)

def _apt_get_install(*packages):
    for package in packages:
        local('sudo apt-get install -q -y {0}'.format(package))

def _git_pull_or_clone(git_repo, git_repo_dir):
    if os.path.isdir(git_repo_dir):
        with lcd(git_repo_dir):
            local('git pull')
            local('git submodule update --init --recursive')
    else:
        local('git clone --recursive {0} {1}'.format(git_repo, git_repo_dir))

