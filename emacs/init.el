;;; Yasser Gonzalez's Emacs Configuration

;; Everything is contained in one Org-babel file that is loaded here.
;; See ~/.emacs.d/config.org for the actual configuration.

(require 'package)
(setq package-enable-at-startup nil)

(require 'org)
(setq vc-follow-symlinks nil)
(defvar my-config-file "~/.emacs.d/config.org")
(org-babel-load-file my-config-file)
