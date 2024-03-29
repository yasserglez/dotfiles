;;; Package management

;; Initialize Emacs built-in package manager
(require 'package)
(setq package-enable-at-startup nil)
(setq package-archives
      '(("gnu" . "http://elpa.gnu.org/packages/")
        ("melpa" . "http://melpa.org/packages/")))
(package-initialize)

;; Install and initialize use-package
(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))

(eval-when-compile
  (require 'use-package))
(require 'use-package-ensure)
(setq use-package-always-ensure t)
(require 'bind-key)


;;; Appearance

;; Solarized color scheme
(use-package solarized-theme
  :init
  ;; Don't change the size of org-mode headlines
  (setq solarized-scale-org-headlines nil)
  ;; Avoid all font-size changes
  (setq solarized-height-minus-1 1.0
        solarized-height-plus-1 1.0
        solarized-height-plus-2 1.0
        solarized-height-plus-3 1.0
        solarized-height-plus-4 1.0)
  (load-theme 'solarized-dark t))

;; Show the buffer name in the window title
(require 'uniquify)
(setq frame-title-format "%b"
      uniquify-buffer-name-style 'forward)

;; Hide the the menubar, toolbar and the scrollbars
(menu-bar-mode -1)
(tool-bar-mode -1)
(scroll-bar-mode -1)

;; Show line and column number in the mode line
(line-number-mode)
(column-number-mode)

;; Alerts
(use-package alert
  :init
  ;; Configure the default style
  (setq alert-default-style 'notifier))


;;; Completion, spell checking, syntax checking, etc

;; Ivy
(use-package ivy
  :config
  (setq ivy-use-virtual-buffers t)
  (setq ivy-use-selectable-prompt t)
  (setq ivy-count-format "(%d/%d) ")
  :init
  (ivy-mode))

(use-package swiper
  :config
  (global-set-key "\C-s" 'swiper))

;; Syntax checking
(use-package flycheck
  :init (global-flycheck-mode)
  :config
  ;; https://emacs.stackexchange.com/q/21664
  (setq-default flycheck-disabled-checkers '(emacs-lisp-checkdoc)))

;; Spell checking
(setq ispell-program-name "aspell"
      ispell-extra-args '("--sug-mode=ultra")
      ispell-dictionary "en"
      ispell-personal-dictionary "~/.emacs.d/aspell.pws")
(add-hook 'text-mode-hook 'flyspell-mode)
(add-hook 'prog-mode-hook 'flyspell-prog-mode)

;; Unset the C-M-i key binding, used for completion in Elpy
(eval-after-load "flyspell"
  '(define-key flyspell-mode-map (kbd "C-M-i") nil))


;;; Git

(use-package magit
  :bind* ("C-c g" . magit-status)
  :config
  (setq magit-completing-read-function 'ivy-completing-read)
  (setq vc-handled-backends nil
        vc-follow-symlinks nil))


;;; Specific file formats

;; Org-mode
(load "~/.emacs.d/init-org.el")

;; Python
(load "~/.emacs.d/init-python.el")

;; YAML
(use-package yaml-mode
  :mode (("\\.yml\\'" . yaml-mode)
         ("\\.yaml\\'" . yaml-mode)))


;;; Misc

(use-package exec-path-from-shell
  :init
  (setq exec-path-from-shell-variables '("PATH"))
  (exec-path-from-shell-initialize))

;; Ask "yes or no" questions with "y or n"
(fset 'yes-or-no-p 'y-or-n-p)

;; Disable confirmations for non-existing files or buffers
(setq confirm-nonexistent-file-or-buffer nil)

;; Disable the splash screen and the echo area message
(setq inhibit-startup-message t
      inhibit-startup-echo-area-message t)

;; Kill a buffer even if it has a process attached to it
(setq kill-buffer-query-functions
      (remq 'process-kill-buffer-query-function
            kill-buffer-query-functions))

;; Disable auto-save and backups
(setq auto-save-default nil)
(setq make-backup-files nil)

;; Enable global auto-revert mode
(global-auto-revert-mode t)

;; Move between windows using the arrow keys
(windmove-default-keybindings)

;; Use the keys next to the space bar as meta
(setq mac-command-modifier 'meta)
(setq mac-option-modifier 'meta)

;; End sentences with one space
(setq sentence-end-double-space nil)

;; Remove trailing whitespaces on save
(add-hook 'before-save-hook 'delete-trailing-whitespace)

;; Require a final newline when saving files
(setq require-final-newline t)

;; Don't use tabs for indentation
(setq-default indent-tabs-mode nil)

;; RET auto-indents by default
(bind-key "RET" 'newline-and-indent)

;; Save customizations in a separate file
(setq custom-file "~/.emacs.d/custom.el")
(load custom-file)
