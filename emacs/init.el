;;; Yasser Gonzalez's Emacs Configuration

;; Everything is contained in one Org-babel file that is loaded here.
(require 'org)
(setq vc-follow-symlinks nil)
(defvar yasserglez/config-file "~/.emacs.d/config.org")
(org-babel-load-file yasserglez/config-file)
