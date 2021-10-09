;;; Task Management based on GTD

(use-package org
  :ensure org-plus-contrib
  :preface
  (defun my-org-agenda-next-week (&optional arg)
    (interactive "P")
    (org-agenda arg "cw"))
  (defun my-org-agenda-today (&optional arg)
    (interactive "P")
    (org-agenda arg "cd"))
  (defun my-org-agenda-tasks (&optional arg)
    (interactive "P")
    (org-agenda arg "ct"))
  :init
  (setq org-modules '(org-checklist org-habit))
  :mode (("\\.org\\'" . org-mode)
         ("\\.org_archive\\'" . org-mode))
  :bind* (("C-c a" . org-agenda)
          ("C-c b" . org-iswitchb)
          ("C-c l" . org-store-link)
          ("<f9>"  . org-capture)
          ("<f10>" . my-org-agenda-tasks)
          ("<f11>" . my-org-agenda-today)
          ("<f12>" . my-org-agenda-next-week)))

;; Tasks marked as TODO are next actions in GTD. TODO tasks may have
;; an associated date or time (for appointments, etc), or I schedule
;; them to be done on a particular day during the weekly review. Tasks
;; marked as MAYBE are things I may want to do in the future – i.e.
;; someday/maybe in GTD. MAYBE tasks turn into TODO tasks when I
;; decide to work on them. TODO tasks can be resolved by marking them
;; as DONE or REF. Tasks marked as DONE can be archived, while REF
;; tasks may be relevant for future reference.

(setq org-use-fast-todo-selection t)
(setq org-todo-keywords
      '((sequence "TODO(t!)" "MAYBE(m!)" "|" "DONE(d!)" "REF(r!)")))

;; Task state changes are logged into a drawer. A timestamp is added
;; every time a task transitions form one state to another.

(setq org-log-into-drawer "LOGBOOK")
(setq org-clock-into-drawer "LOGBOOK")
(setq org-log-redeadline 'time)
(setq org-log-reschedule 'time)
(setq org-log-repeat 'time)

;; inbox.org is used for capturing tasks (via capture templates and a
;; few IFTTT recipes that append content to that file). I keep
;; separate files for the different projects (containing headers for
;; tasks and reference materials). Each file has a #+FILETAGS header
;; so it is easier to filter tasks for a particular project using tags
;; in the agenda.

(setq org-agenda-files '("~/Dropbox/org/"))

(setq org-directory "~/Dropbox/org/")
(setq org-default-notes-file "~/Dropbox/org/inbox.org")

(setq org-capture-templates
      '(("t" "Task" entry (file "")
         "* TODO %?\n  :LOGBOOK:\n  - State \"TODO\"                         %U\n  :END:")
        ("r" "Reference" entry (file "")
         "* REF %?\n  :LOGBOOK:\n  - State \"REF\"                    %U\n  :END:")))

(setq org-refile-targets '((org-agenda-files :level . 1)))

;; Configure a group of agenda views and key bindings for quick access.

(setq org-agenda-repeating-timestamp-show-all t
      org-agenda-remove-tags t
      org-agenda-show-all-dates t
      org-agenda-skip-deadline-if-done t
      org-agenda-skip-deadline-prewarning-if-scheduled t
      org-agenda-skip-scheduled-if-done t
      org-agenda-start-on-weekday nil)

(setq org-agenda-custom-commands
      '(("c" . "Custom agenda commands")
        ("cd" "Agenda for today" agenda ""
         ((org-agenda-compact-blocks t)
          (org-agenda-span 1)
          (org-deadline-warning-days 0)))
        ("cw" "Agenda for next week" agenda ""
         ((org-agenda-compact-blocks t)
          (org-agenda-span 7)
          (org-deadline-warning-days 14)))
        ("ct" "Unscheduled tasks" todo "TODO"
         ((org-agenda-overriding-header "Unscheduled tasks: ")
          (org-agenda-skip-function '(org-agenda-skip-subtree-if 'timestamp))))))

;; Habits

(require 'org-habit)

(setq org-habit-preceding-days 14)
(setq org-habit-following-days 1)
(setq org-habit-show-habits-only-for-today t)
(setq org-habit-show-all-today nil)

(setq org-habit-graph-column 40)
(setq org-habit-completed-glyph ?x)
(setq org-habit-today-glyph ? )
(setq org-habit-show-done-always-green t)
(set-face-attribute 'org-habit-clear-face nil
                    :foreground "#859900"
                    :background "#5b7300")

;; Holidays

(setq holiday-local-holidays
      '((holiday-fixed 2 14 "Valentine's Day")
        (holiday-fixed 4 1 "April Fools' Day")
        (holiday-float 5 0 2 "Mother's Day")
        (holiday-float 6 0 3 "Father's Day")
        (holiday-fixed 10 31 "Halloween")
        (holiday-fixed 12 31 "New Year's Eve")
        ;; Ontario Public Holidays
        ;; http://www.labour.gov.on.ca/english/es/pubs/guide/publicholidays.php
        (holiday-fixed 1 1 "New Year's Day")      ; January 1
        (holiday-float 2 1 3 "Family Day")        ; Third Monday in February
        (holiday-easter-etc -2 "Good Friday")     ; Friday before Easter Sunday
        (holiday-float 5 1 -1 "Victoria Day" 24)  ; Monday before May 25
        (holiday-fixed 7 1 "Canada Day")          ; July 1
        (holiday-float 8 1 1 "Civic Holiday")     ; First Monday in August
        (holiday-float 9 1 1 "Labour Day")        ; First Monday in September
        (holiday-float 10 1 2 "Thanksgiving Day") ; Second Monday in October
        (holiday-fixed 12 25 "Christmas Day")     ; Christmas Day
        (holiday-fixed 12 26 "Boxing Day")))      ; Boxing Day

(setq holiday-other-holidays '())

;; Regenerate calendar-holidays.
(setq calendar-holidays
      (append holiday-local-holidays
              holiday-other-holidays))

;; Encryption

(require 'org-crypt)

;; Use a hook to automatically encrypt entries before a file is saved
(org-crypt-use-before-save-magic)

;; GPG key used for encryption
(setq org-crypt-key "97DF6096")

;; Encrypted entries are marked with the private tag. Excluding the
;; private tag from inheritance prevents text already encrypted from
;; being encrypted again.
(setq org-crypt-tag-matcher "private")
(setq org-tags-exclude-from-inheritance '("private"))

;; Misc

;; Save all Org-mode buffers at one minute before the hour
;; This is used in combination with the bin/org-sync shell script.
(run-at-time "00:59" (* 60 60) 'org-save-all-org-buffers)

;; Don’t split lines with M-RET
(setq org-M-RET-may-split-line nil)

;; Show hours and minutes in clock tables
(setq org-time-clocksum-format
      '(:hours "%d" :require-hours t :minutes ":%02d" :require-minutes t))

;; Only record the time when a task is archived
(setq org-archive-save-context-info '(time))
