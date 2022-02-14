(use-package elpy
  :init
  ;; Disable some of the default modules.
  (setq elpy-modules '(elpy-module-sane-defaults
                       elpy-module-company
                       elpy-module-eldoc
                       elpy-module-pyvenv))
  (elpy-enable)
  :config
  ;; Use flycheck instead of flymake.
  (add-hook 'elpy-mode-hook 'flycheck-mode)
  ;; Use black for code formatting.
  (setq elpy-formatter 'black)
  ;; Integrate pyenv virtualenvs.
  (setenv "WORKON_HOME" "~/.pyenv/versions/")
  (defalias 'pyenv-activate 'pyvenv-workon)
  (defalias 'pyenv-deactivate 'pyvenv-deactivate))
