# oh-my-zsh configuration

export ZSH=$HOME/.oh-my-zsh

SOLARIZED_THEME="light"
ZSH_THEME="blinks"

plugins=(command-not-found git python pip fabric)
source $ZSH/oh-my-zsh.sh

# Customize the blinks theme

PROMPT='%{%f%k%b%}
%{%K{${bkg}}%B%F{green}%}%n%{%B%F{blue}%}@%{%B%F{cyan}%}%m%{%B%F{green}%} %{%b%F{yellow}%K{${bkg}}%}%~%{%B%F{green}%}$(git_prompt_info)%E%{%f%k%b%}
%{%K{${bkg}}%} %#%{%f%k%b%} '
RPROMPT=''

# Same colors in ls and zsh completions

eval `dircolors ~/.dircolors`
alias ls='ls --color=auto'
zstyle ':completion:*' list-colors "${(@s.:.)LS_COLORS}"
autoload -Uz compinit
compinit

# $PATH settings

export PATH="$HOME/.local/bin:$PATH"
