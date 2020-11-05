;;;; A Hy file to read the config file of the email sending
;;;; See more, from the docs
"[sender]
address = <example@example.com>
password = your password or smtp password
[email]
smtp-host = smtp.example.com
smtp-port = 465
[receive]
use = pop3 or imap
pop3-host = pop3.example.com
imap-host = imap.example.com
pop3-port = 435
imap-host = 211
download-path = /folder/for/downloads
"

(import configparser click os)

(setv config (.ConfigParser configparser))

(setv Config {})

(defn reader [config-file]
	(setv file (os.path.abspath config-file))
	(.read config file, :encoding "utf-8")
	(setv conf {})
	(setv	(get conf "address") (.get config "sender" "address")
		(get conf "password") (.get config "sender" "password")
		(get conf "smtp-host") (.get config "email" "smtp-host")
		(get conf "smtp-port") (.getint config "email" "smtp-port")
		(get conf "use") (.get config "receive" "use")
		use (get conf "use")
	)
	(cond	[(= use "pop3") (do 
					(setv (get conf "re-host") (.get config "receive" "pop3-host"))
					(setv (get conf "re-port") (.getint config "receive" "pop3-port")
				)
		]
		[(= use "impa") (do 
					(setv (get conf "re-host") (.get config "receive" "imap-host"))
					(setv (get conf "re-port") (.getint config "receive" "imap-port"))
				)
		]
	)
	(setv (get conf "download") (.get config "receive" "download-path"))
	(setv Config conf)
	(return Config)
)