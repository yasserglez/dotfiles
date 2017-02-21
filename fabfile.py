import os

from fabric.api import lcd, local
from fabric.contrib.console import confirm


def all(force=False):
    apt(force)
    zsh(force)
    bin(force)
    solarized(force)
    git(force)
    emacs(force)
    vim(force)
    python(force)
    R(force)
    scala(force)


def apt(force=False):
    with lcd('apt'):
        if force or _can_overwrite('/etc/apt/sources.list'):
            local('sudo ln -sf $PWD/sources.list /etc/apt/sources.list')
        if force or _can_overwrite('/etc/apt/sources.list.d/'):
            local('sudo rm -fr /etc/apt/sources.list.d')
            local('sudo ln -s $PWD/sources.list.d /etc/apt/sources.list.d')
    _apt_get_update()
    _apt_get_install('launchpad-getkeys')
    local('sudo launchpad-getkeys')
    local('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 642AC823')


def bin(force=False):
    local_bin = '~/.local/bin'
    local('mkdir -p {}'.format(local_bin))
    for bin_file in os.listdir('bin'):
        bin_path = os.path.join(local_bin, bin_file)
        if force or _can_overwrite(bin_path):
            with lcd('bin'):
                local('ln -sf $PWD/{} {}'.format(bin_file, bin_path))


def emacs(force=False):
    _apt_get_install('emacs')
    if force or _can_overwrite('~/.emacs.d'):
        local('rm -fr ~/.emacs.d')
        local('mkdir -p ~/.emacs.d')
        with lcd('emacs'):
            local('ln -s $PWD/init.el ~/.emacs.d/init.el')
            local('ln -s $PWD/config.org ~/.emacs.d/config.org')
            local('ln -s $PWD/snippets ~/.emacs.d/snippets')
            local('ln -s $PWD/aspell.pws ~/.emacs.d/aspell.pws')


def git(force=False):
    _apt_get_install('git')
    if force or _can_overwrite('~/.gitconfig'):
        with lcd('git'):
            local('ln -sf $PWD/gitconfig ~/.gitconfig')
    if force or _can_overwrite('~/.gitignore'):
        local('rm -f ~/.gitignore')
        git_repo = 'https://github.com/github/gitignore'
        git_repo_dir = 'git/gitignore'
        _git_pull_or_clone(git_repo, git_repo_dir)
        with lcd(git_repo_dir):
            templates = ('Global/Linux', 'Global/Vim', 'Global/Emacs',
                         'Global/Eclipse', 'Global/Matlab', 'R',
                         'Python', 'C', 'C++', 'Java', 'Scala', 'TeX')
            for template in templates:
                local('cat {}.gitignore >> ~/.gitignore'.format(template))


def R(force=False):
    _apt_get_install('r-base', 'r-base-dev')
    local('mkdir -p ~/.local/lib/R/library')
    if force or _can_overwrite('~/.Rprofile'):
        with lcd('R'):
            local('ln -sf $PWD/Rprofile ~/.Rprofile')


def python(force=False):
    _apt_get_install('python', 'python-pip', 'python3', 'python3-pip')
    local('pip install --user --upgrade virtualenv virtualenvwrapper')


def scala(force=False):
    _apt_get_install('scala', 'sbt')
    if force or _can_overwrite('~/.sbt'):
        local('rm -fr ~/.sbt')
        local('ln -s $PWD/sbt ~/.sbt')


def solarized(force=False, scheme='dark'):
    # gnome-terminal:
    _apt_get_install('gnome-terminal', 'dconf-cli')
    git_repo = 'https://github.com/anthony25/gnome-terminal-colors-solarized'
    git_repo_dir = 'solarized/gnome-terminal-colors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        local('./install.sh -s {} -p Default'.format(scheme))

    # dircolors:
    _apt_get_install('coreutils')
    git_repo = 'https://github.com/seebi/dircolors-solarized'
    git_repo_dir = 'solarized/dircolors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    if force or _can_overwrite('~/.dir_colors'):
        with lcd(git_repo_dir):
            local('ln -sf $PWD/dircolors.ansi-{} ~/.dir_colors'.format(scheme))

    # gedit:
    _apt_get_install('gedit')
    git_repo = 'https://github.com/mattcan/solarized-gedit'
    git_repo_dir = 'solarized/solarized-gedit'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        local('mkdir -p ~/.local/share/gedit/styles')
        local('ln -sf $PWD/solarized-{}.xml ~/.local/share/gedit/styles/'.format(scheme))

    # IntelliJ:
    git_repo = 'https://github.com/jkaving/intellij-colors-solarized'
    git_repo_dir = 'solarized/intellij-colors-solarized'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd(git_repo_dir):
        for d in os.listdir(os.path.expanduser('~')):
            if d.startswith('.PyCharm') or d.startswith('.IdeaIC'):
                colors_dir = '~/{}/config/colors'.format(d)
                local('mkdir -p {}'.format(colors_dir))
                local('ln -sf "$PWD/Solarized {}.icls" {}/'.format(scheme.title(), colors_dir))


def vim(force=False):
    _apt_get_install('git', 'vim-nox')
    if force or _can_overwrite('~/.vimrc'):
        with lcd('vim'):
            local('ln -sf "$PWD/vimrc" ~/.vimrc')
    if force or _can_overwrite('~/.vim'):
        local('rm -fr ~/.vim')
        local('mkdir -p ~/.vim')
        git_repo = 'https://github.com/gmarik/Vundle.vim'
        git_repo_dir = 'vim/vundle/Vundle.vim'
        _git_pull_or_clone(git_repo, git_repo_dir)
        with lcd('vim'):
            local('ln -sf $PWD/vundle ~/.vim/vundle')


def zsh(force=False):
    _apt_get_install('zsh')
    local('chsh -s /usr/bin/zsh')
    git_repo = 'https://github.com/zsh-users/prezto'
    git_repo_dir = 'zsh/prezto'
    _git_pull_or_clone(git_repo, git_repo_dir)
    with lcd('zsh'):
        if force or _can_overwrite('~/.zprezto'):
            local('ln -sf $PWD/prezto ~/.zprezto')
            local('ln -sf $PWD/prompt_yasserglez_setup ~/.zprezto/modules/prompt/functions/')
        for dotfile in ('zlogin', 'zlogout', 'zpreztorc', 'zprofile', 'profile', 'zshenv', 'zshrc'):
            if force or _can_overwrite('~/.{}'.format(dotfile)):
                local('rm -f ~/.{}'.format(dotfile))
                local('ln -sf $PWD/{0} ~/.{0}'.format(dotfile))


def _can_overwrite(file_or_dir):
    file_or_dir = os.path.expanduser(file_or_dir)
    msg = 'Overwrite {}?'.format(file_or_dir)
    return not os.path.exists(file_or_dir) or confirm(msg)


def _apt_get_update():
    local('sudo apt-get update')


def _apt_get_install(*packages):
    for package in packages:
        local('sudo apt-get install --yes {}'.format(package))


def _git_pull_or_clone(git_repo, git_repo_dir):
    if os.path.isdir(git_repo_dir):
        with lcd(git_repo_dir):
            local('git pull')
            local('git submodule update --init --recursive')
    else:
        local('git clone --recursive {} {}'.format(git_repo, git_repo_dir))
