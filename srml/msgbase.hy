(import [difflib [SequenceMatcher]])

(defclass MSG [object]
	(setv MSG "A base object for sended or recived messages")
	(defn --eq-- [self ot]
		(if (isinstance ot MSG)
			(do
				(setv rate (.quick-ratio (SequenceMatcher :a self.raw :b ot.raw)))
				(if (> rate 0.9)
					(return True)
					(return False)
				)
			)
			(raise (TypeError "MSG object can't compare with other types"))
		)
	)
)
