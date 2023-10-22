(use-package elpy
  :init
  ;; Disable some of the default modules.
  (setq elpy-modules '(elpy-module-sane-defaults
                       elpy-module-company
                       elpy-module-eldoc
                       elpy-module-pyvenv))
  (elpy-enable)
  :config
  ;; RPC process.
  (setq elpy-rpc-python-command "/usr/bin/python3")
  (setq elpy-rpc-virtualenv-path 'default)
  ;; Integrate pyenv virtualenvs.
  (setenv "WORKON_HOME" "~/.pyenv/versions/")
  (defalias 'pyenv-activate 'pyvenv-workon)
  (defalias 'pyenv-deactivate 'pyvenv-deactivate)
  ;; Use flycheck instead of flymake.
  (add-hook 'elpy-mode-hook 'flycheck-mode)
  ;; Use black for code formatting.
  (setq elpy-formatter 'black))
