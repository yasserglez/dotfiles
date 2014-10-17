from fabric.api import *


def solarized(scheme='light'):
    solarized_gnome_terminal(scheme)


def solarized_gnome_terminal(scheme='light'):
    with lcd('gnome-terminal-colors-solarized'):
        local('sudo apt-get install -y dconf-cli')
        local('./install.sh -s {scheme} -p Default'.format(scheme=scheme))
