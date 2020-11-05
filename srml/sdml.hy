;; Hy Lisp to send-mail
(import logging time)
(import os sys codecs smtplib [. [mime]])

(import [email.utils [parseaddr formatdate formataddr make-msgid]]
	[email.header [Header]]
	[markdown [markdown]])
;;(import rdconf)

(setv logger logging)

;;(setv baseconfig (.reader rdconf))

(defn sanitize-address [addr &optional [encoding "utf-8"]]
	"sanitize one email address for sending email"
	(if* (isinstance addr str)
		(setv addr (parseaddr addr))
	)
	(setv [nm addr] addr)
	(setv nm (.encode (Header nm encoding)))
	;;(setv addr (.encode addr "ascii"))
	(return (formataddr (, nm addr)))
)
(defn sanitize-addresses [addresses &optional [encoding "utf-8"]]
	"sanitize some email address for sending email, return a generation"
	(defn ana [e] (sanitize-address e encoding))
	(return (gfor e addresses (ana e)))
)

(defn sanitize-subject [subject &optional [encoding "utf-8"]]
	(try (.encode subject "ascii")
	(except [Exception] (try (setv subject (.encode (Header subject encoding)))
	(except [Exception] (setv subject (.encode (Header subject "utf-8"))))
	)))
	(return subject)
)

(defn smtpconnect [smtp-host send-mail token-passwd &optional [port 465]]
	(try
		(.info logger "connecting to smtp...")
		(setv smtp (.SMTP_SSL smtplib smtp-host port))
		(.info logger "succeed connect with ssl")
	(except [Exception] (setv smtp (.SMTP smtplib smtp-host port)) (.info logger "succeed connect but without ssl"))
	)
	(.info logger "connect to" smtp-host ", with port:" port)
	;;(.connect smtp smtp-host port)
	(.connect smtp "smtp.163.com" 465)
	(.ehlo smtp)
	(.login smtp send-mail token-passwd)
	(return smtp)
)

(defn easy-mail-sender [smtp-host passwd send-mail tos subject content &optional [files-path []]]
	(setv msg (.MIMEMultipart mime.multipart))
	(setv (get msg "From") send-mail)
	(setv 	(get msg "To") (.join ", " (list (set(sanitize-addresses tos))))
		(get msg "Subject") subject
		content (.text.MIMEText mime content "plain" "utf-8")
	)
	(.attach msg content)
	(.info logger "add files")
	(for [file files-path]
		(setv part (.application.MIMEApplication mime (.read (.open codecs file "rb"))))
		(.add_header part "Content-Disposition" "attachment" 
			:filename (os.path.basename (os.path.abspath file)))
		(.attach msg part)
		(.info logger "add" file "finish")
	)
	(.info logger "sending...")
	(setv smtp (smtpconnect smtp-host send-mail passwd))
	(.sendmail smtp send-mail tos (str msg))
	(.close smtp)
	(.info logger "sending finish, \ncheck your email box to have a look")
	;;(return smtp)
)

(defn mdToHtml [file]
	(try
		(setv f (.open codecs "r" "utf-8"))
		(return (markdown (.read f)))
	(except [Exception]
		(return None)
	))
)
(defn readFile [file]
	(try
		(return (.read (.open codecs "r" "utf-8")))
	(except [Exception]
		(return None)
	))
)

(defclass Message [object]
	(defn __init__ [self &optional	[subject ""]
		recipients
		body
		html
		mkd
		sender
		reply-to
		date
		files
		charset]
		"Class an email message, noticed that the html or the mkd param must be string"
		(setv	self.sender (or sender "")
			self.subject subject
			self.reci (or recipients [])
			self.body (or body "")
			self.html (or html "")
			self.mkd (or mkd "")
			self.reply-to reply-to
			self.date (or date (.time time))
			self.char charset
			self.files (or files [])
			self.msgID (make-msgid)
		)
		(.info logger "Message create")
	)
	(defn _mimetext [self text &optional [subtype "plain"]]
		"create MIMEText class with the given subtype"
		(.MIMEText mime.text text :_subtype subtype :_charset (or self.char "utf-8"))
	)
	(defn as-string [self] (return (.as-string (._message self))))
	(defn as-bytes [self] (return (.as-bytes (._message self))))
	(defn __str__ [self] (return (.as-string self)))
	(defn __bytes__ [self] (return (.as-bytes self)))
	(defn sned_to [self] (return (set self.reci)))
	(defn _message [self]
		"Create the email"
		(setv encode (or self.char "utf-8")) ; set the encoding

		(if (and (= (len self.files) 0) (not (or self.html self.mkd))) ; if not file, only plain text
			(setv msg (._mimetext self self.body))
		(if (and (> (len self.files) 0) (not (or self.html self.mkd))) ; if has file, only plain text
			(do 	(setv msg (.MIMEMultipart mime.multipart))
				(.attach msg (._mimetext self self.body))
			)
		(do	(setv	msg (.MIMEMultipart mime.multipart)		;if has file and noy only plain text but also html or mkd content
				alter (.MIMEMultipart mime.multipart "alternative"))
			(.attach alter (._mimetext self self.body "plain"))
			(setv html (+ self.html (markdown self.mkd)))
			;;(print md)
			(if* html (.attach alter (._mimetext self html "html")))
			(.attach msg alter)
		)))
		;;(print self)
		;; add subject
		(setv subject (sanitize-subject self.subject encode))
		(setv (get msg "Subject") subject)

		;; add from and to
		(setv 	(get msg "From") (sanitize-address self.sender encode)
			(get msg "To") (.join ", " (list (set (sanitize-addresses self.reci))))
			(get msg "Date") (formatdate self.date :localtime 1)
			(get msg "Message-ID") self.msgID
		)
		;; add reply context
		(if* self.reply-to
			(setv (get msg "Reply-To")(sanitize-address self.reply-to encode)))

		;; add files
		(for [file self.files]
			(if-not file break)
			;;(print "add:" file)
			(setv part (.application.MIMEApplication mime (.read (.open codecs file "rb"))))
			(.add_header part "Content-Disposition" "attachment"
				:filename (os.path.basename (os.path.abspath file)))
			(.attach msg part)
		)
		(return msg)
	)
	#@(property
	(defn mail [self]
		(if (isinstance self.sender str)
			(return self.sender)
			(return (get self.sender 1))
		)
	))
)

(defclass Connect []
	(defn __init__ [self smtp-host &optional mails [smtp-port 465] [ssl True]]
		(if* mails (setv [self.mail self.passwd] mails))
		(setv self.host smtp-host self.port smtp-port)
		(if ssl (try
			(setv self.smtp (.SMTP_SSL smtplib smtp-host smtp-port))
		(except [Exception]
			(setv self.smtp (.SMTP smtplib smtp-host smtp-port))
		))
		(setv self.smtp (.SMTP smtplib smtp-host smtp-port)))
	)
	(defn login [self mail passwd]
		(setv self.mail mail self.passwd passwd)
		(.connect self.smtp self.host self.port)
		(.ehlo self.smtp)
		(.login self.smtp mail passwd)
	)
	(defn send [self message]
		(.sendmail self.smtp message.mail (set message.reci) (str message))
	)
	(defn close [self]
		(.close self.smtp)
	)
	(defn __enter__ [self]
		;;(print "--enter-- called")
		(.login self self.mail self.passwd)
		(return self)
	)
	(defn __exit__ [self exc-type exc-val tb]
		;;(print "--exit-- called")
		(.close self)
	)
)
