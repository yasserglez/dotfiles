# ~/.zlogin: This file is sourced by login shells after zshrc, and thus, it 
# should contain commands that need to execute at login. This is not the 
# file to define aliases, functions, shell options, and key bindings. 
# It should not change the shell environment.

# Execute code that does not affect the current session in the background.
{
  # Compile the completion dump to increase startup speed.
  zcompdump="${ZDOTDIR:-$HOME}/.zcompdump"
  if [[ -s "$zcompdump" && (! -s "${zcompdump}.zwc" || "$zcompdump" -nt "${zcompdump}.zwc") ]]; then
    zcompile "$zcompdump"
  fi
} &!
