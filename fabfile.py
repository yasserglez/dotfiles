from fabric.api import *


def solarized(scheme='light'):
    solarized_dircolors(scheme)
    solarized_gnome_terminal(scheme)

def solarized_gnome_terminal(scheme='light'):
    with lcd('gnome-terminal-colors-solarized'):
        local('sudo apt-get install -y dconf-cli')
        local('./install.sh -s {scheme} -p Default'.format(scheme=scheme))
        
def solarized_dircolors(scheme='light'):
    with lcd('dircolors-solarized'):
        local('rm -f ~/.dircolors')
        local('ln -s "$PWD/dircolors.ansi-{scheme}" ~/.dircolors'.format(scheme=scheme))
        local('eval `dircolors ~/.dircolors`')
