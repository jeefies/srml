(import [email.mime [	multipart
			application
			image
			nonmultipart
			text
			base
			audio
			message
			]
	]
)
(setv	MIMEMultipart multipart.MIMEMultipart
	MIMEApplication application.MIMEApplication
	MIMEImage image.MIMEImage
	MIMEBase base.MIMEBase
	MIMEAudio audio.MIMEAudio
	MIMEMessage message.MIMEMessage)
