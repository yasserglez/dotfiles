
% oh-my-zsh configuration

export ZSH=$HOME/.oh-my-zsh
ZSH_THEME="blinks"
plugins=(command-not-found git python pip fabric)
source $ZSH/oh-my-zsh.sh

# Customize the blinks theme

SOLARIZED_THEME="light"
PROMPT='%{%f%k%b%}
%{%K{${bkg}}%B%F{green}%}%n%{%B%F{blue}%}@%{%B%F{cyan}%}%m%{%B%F{green}%} %{%b%F{yellow}%K{${bkg}}%}%~%{%B%F{green}%}$(git_prompt_info)%E%{%f%k%b%}
%{%K{${bkg}}%} %#%{%f%k%b%} '
RPROMPT=''

# Setting the PATH

# 'pip --user' installed packages
export PATH=/home/ygf/.local/bin:$PATH
