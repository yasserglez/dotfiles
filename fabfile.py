import os

from fabric.api import lcd, local
from fabric.contrib.console import confirm


def install_all(force=False):
    install_zsh(force)
    install_git(force)
    install_emacs(force)
    install_vim(force)
    install_solarized_gnome_terminal(force)
    install_solarized_dircolors(force)
    install_solarized_gedit(force)
    install_r(force)


def install_r(force=False):
    _apt_get_install('r-base', 'r-base-dev')
    if force or _can_overwrite('~/.Rprofile'):
        local('rm -f ~/.Rprofile')
        local('mkdir -p ~/.local/lib/R/library')
        with lcd('R'):
            local('ln -s $PWD/Rprofile ~/.Rprofile')


def install_emacs(force=False):
    _apt_get_install('emacs24')
    if force or _can_overwrite('~/.emacs.d'):
        local('rm -rf ~/.emacs.d')
        local('mkdir ~/.emacs.d')
        with lcd('emacs'):
            local('ln -s $PWD/init.el ~/.emacs.d/init.el')
            local('ln -s $PWD/config.org ~/.emacs.d/config.org')


def install_vim(force=False):
    _apt_get_install('git', 'vim-nox')
    if force or _can_overwrite('~/.vimrc'):
        with lcd('vim'):
            local('rm -f ~/.vimrc')
            local('ln -sf "$PWD/vimrc" ~/.vimrc')
    if force or _can_overwrite('~/.vim'):
        local('rm -rf ~/.vim')
        local('mkdir ~/.vim')
        git_repo = 'https://github.com/gmarik/Vundle.vim'
        git_repo_dir = 'vim/vundle/Vundle.vim'
        _git_pull_or_clone(git_repo, git_repo_dir)
        with lcd('vim'):
            local('ln -sf $PWD/vundle ~/.vim/vundle')


def install_git(force=False):
    _apt_get_install('git')
    if force or _can_overwrite('~/.gitconfig'):
        with lcd('git'):
            local('rm -f ~/.gitconfig')
            local('ln -sf $PWD/gitconfig ~/.gitconfig')
    if force or _can_overwrite('~/.gitignore'):
        local('rm -f ~/.gitignore')
        git_repo = 'https://github.com/github/gitignore'
        git_repo_dir = 'git/gitignore'
        _git_pull_or_clone(git_repo, git_repo_dir)
        with lcd(git_repo_dir):
            templates = ('Global/Linux', 'Global/vim', 'Global/Emacs',
                         'Global/Eclipse', 'Global/Matlab', 'R',
                         'Python', 'C', 'C++', 'Java', 'TeX')
            for template in templates:
                local('cat {0}.gitignore >> ~/.gitignore'.format(template))


def install_zsh(force=False):
    _apt_get_install('zsh', 'xcape')
    local('chsh -s /usr/bin/zsh')
    git_repo = 'https://github.com/sorin-ionescu/prezto'
    git_repo_dir = 'zsh/prezto'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd('zsh'):
        if force or _can_overwrite('~/.zprezto'):
            local('rm -fr ~/.zprezto')
            local('ln -s $PWD/prezto ~/.zprezto')
            local('ln -sf $PWD/prompt_yasserglez_setup ~/.zprezto/modules/prompt/functions/')
        for dotfile in ('zlogin', 'zlogout', 'zpreztorc', 'zprofile', 'profile', 'zshenv', 'zshrc'):
            if force or _can_overwrite('~/.{0}'.format(dotfile)):
                local('rm -f ~/.{0}'.format(dotfile))
                local('ln -sf $PWD/{0} ~/.{0}'.format(dotfile))


def install_solarized_gnome_terminal(force=False, scheme='dark'):
    _apt_get_install('gnome-terminal', 'dconf-cli')
    git_repo = 'https://github.com/anthony25/gnome-terminal-colors-solarized'
    git_repo_dir = 'solarized/gnome-terminal-colors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        local('./install.sh -s {0} -p Default'.format(scheme))


def install_solarized_dircolors(force=False, scheme='dark'):
    _apt_get_install('coreutils')
    git_repo = 'https://github.com/seebi/dircolors-solarized'
    git_repo_dir = 'solarized/dircolors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    if force or _can_overwrite('~/.dir_colors'):
        with lcd(git_repo_dir):
            local('rm -f ~/.dir_colors')
            local('ln -s $PWD/dircolors.ansi-{0} ~/.dir_colors'.format(scheme))


def install_solarized_gedit(force=False, scheme='dark'):
    _apt_get_install('gedit')
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
        local('sudo apt-get install --yes --force-yes {0}'.format(package))


def _git_pull_or_clone(git_repo, git_repo_dir):
    if os.path.isdir(git_repo_dir):
        with lcd(git_repo_dir):
            local('git pull')
            local('git submodule update --init --recursive')
    else:
        local('git clone --recursive {0} {1}'.format(git_repo, git_repo_dir))
