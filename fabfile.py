from fabric.api import *


def oh_my_zsh():
    local('sudo apt-get install -y zsh')
    local('rm -f ~/.oh-my-zsh')
    local('ln -sf "$PWD/oh-my-zsh" ~/.oh-my-zsh')
    local('chsh -s /bin/zsh')
    local('ln -sf "$PWD/zshrc" ~/.zshrc')

def solarized(scheme='dark'):
    solarized_dircolors(scheme)
    solarized_gnome_terminal(scheme)
    solarized_gedit(scheme)

def solarized_gnome_terminal(scheme='dark'):
    with lcd('gnome-terminal-colors-solarized'):
        local('sudo apt-get install -y dconf-cli')
        local('./install.sh -s {scheme} -p Default'.format(scheme=scheme))
        
def solarized_dircolors(scheme='dark'):
    with lcd('dircolors-solarized'):
        local('rm -f ~/.dircolors')
        local('ln -s "$PWD/dircolors.ansi-{scheme}" ~/.dircolors'.format(scheme=scheme))
        local('eval `dircolors ~/.dircolors`')
        
def solarized_gedit(scheme='dark'):
    with lcd('solarized-gedit'):
        local('mkdir -p ~/.local/share/gedit/styles')
        local('ln -sf "$PWD/solarized-dark.xml" ~/.local/share/gedit/styles/')
        local('ln -sf "$PWD/solarized-dark.xml" ~/.local/share/gedit/styles/')

