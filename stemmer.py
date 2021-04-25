#############################################

class Stemmer:
	def __init__(self):
		self.word = ""  # buffer for word to be stemmed
		self.index = 0
		self.first = 0
		self.offset = 0   # is a general offset into the string

	#########################################

	def remove_plurals_ing_ed(self):
		if self.word[self.index] == 's':
			if self.ends("sses"):
				self.index = self.index - 2
			elif self.ends("ies"):
				self.set_to("i")
			elif self.word[self.index - 1] != 's':
				self.index = self.index - 1
		if self.ends("eed"):
			if self.measure() > 0:
				self.index = self.index - 1
		elif (self.ends("ed") or self.ends("ing")) and self.vowel_in_stem():
			self.index = self.offset
			if self.ends("at"):   self.set_to("ate")
			elif self.ends("bl"): self.set_to("ble")
			elif self.ends("iz"): self.set_to("ize")
			elif self.double_c(self.index):
				self.index = self.index - 1
				ch = self.word[self.index]
				if ch == 'l' or ch == 's' or ch == 'z':
					self.index = self.index + 1
			elif (self.measure() == 1 and self.cvc(self.index)):
				self.set_to("e")

	#########################################

	def is_consonant(self, index):
		"""cons(i) is TRUE <=> b[i] is a consonant."""
		if self.word[index] == 'a' or self.word[index] == 'e' or self.word[index] == 'i' or self.word[index] == 'o' or self.word[index] == 'u':
			return 0
		if self.word[index] == 'y':
			if index == self.first:
				return 1
			else:
				return (not self.is_consonant(index - 1))
		return 1

	#########################################

	def vowel_in_stem(self):
		"""vowel_in_stem() is TRUE <=> k0,...j contains a vowel"""
		for i in range(self.first, self.offset + 1):
			if not self.is_consonant(i):
				return 1
		return 0

	#########################################

	def measure(self):
		n = 0
		i = self.first
		while 1:
			if i > self.offset:
				return n
			if not self.is_consonant(i):
				break
			i = i + 1
		i = i + 1
		while 1:
			while 1:
				if i > self.offset:
					return n
				if self.is_consonant(i):
					break
				i = i + 1
			i = i + 1
			n = n + 1
			while 1:
				if i > self.offset:
					return n
				if not self.is_consonant(i):
					break
				i = i + 1
			i = i + 1

	#########################################

	def double_c(self, j):
		"""doublec(j) is TRUE <=> j,(j-1) contain a double consonant."""
		if j < (self.first + 1):
			return 0
		if (self.word[j] != self.word[j-1]):
			return 0
		return self.is_consonant(j)

	#########################################

	def cvc(self, i):
		if i < (self.first + 2) or not self.is_consonant(i) or self.is_consonant(i-1) or not self.is_consonant(i-2):
			return 0
		ch = self.word[i]
		if ch == 'w' or ch == 'x' or ch == 'y':
			return 0
		return 1

	#########################################

	def ends(self, s):
		length = len(s)
		if s[length - 1] != self.word[self.index]: # tiny speed-up
			return 0
		if length > (self.index - self.first + 1):
			return 0
		if self.word[self.index-length+1:self.index+1] != s:
			return 0
		self.offset = self.index - length
		return 1

	#########################################

	def set_to(self, s):
		length = len(s)
		self.word = self.word[:self.offset+1] + s + self.word[self.offset+length+1:]
		self.index = self.offset + length

	#########################################

	def r(self, s):
		if self.measure() > 0:
			self.set_to(s)

	#########################################

	def set_y_to_i(self):
		if (self.ends("y") and self.vowel_in_stem()):
			self.word = self.word[:self.index] + 'i' + self.word[self.index+1:]

	#########################################

	def double_suffix_to_single(self):
		if self.word[self.index - 1] == 'a':
			if self.ends("ational"):   self.r("ate")
			elif self.ends("tional"):  self.r("tion")
		elif self.word[self.index - 1] == 'c':
			if self.ends("enci"):      self.r("ence")
			elif self.ends("anci"):    self.r("ance")
		elif self.word[self.index - 1] == 'e':
			if self.ends("izer"):      self.r("ize")
		elif self.word[self.index - 1] == 'l':
			if self.ends("bli"):       self.r("ble") 

			elif self.ends("alli"):    self.r("al")
			elif self.ends("entli"):   self.r("ent")
			elif self.ends("eli"):     self.r("e")
			elif self.ends("ousli"):   self.r("ous")
		elif self.word[self.index - 1] == 'o':
			if self.ends("ization"):   self.r("ize")
			elif self.ends("ation"):   self.r("ate")
			elif self.ends("ator"):    self.r("ate")
		elif self.word[self.index - 1] == 's':
			if self.ends("alism"):     self.r("al")
			elif self.ends("iveness"): self.r("ive")
			elif self.ends("fulness"): self.r("ful")
			elif self.ends("ousness"): self.r("ous")
		elif self.word[self.index - 1] == 't':
			if self.ends("aliti"):     self.r("al")
			elif self.ends("iviti"):   self.r("ive")
			elif self.ends("biliti"):  self.r("ble")
		elif self.word[self.index - 1] == 'g': 
			if self.ends("logi"):      self.r("log")

	#########################################

	def remove_full_ness(self):
		if self.word[self.index] == 'e':
			if self.ends("icate"):     self.r("ic")
			elif self.ends("ative"):   self.r("")
			elif self.ends("alize"):   self.r("al")
		elif self.word[self.index] == 'i':
			if self.ends("iciti"):     self.r("ic")
		elif self.word[self.index] == 'l':
			if self.ends("ical"):      self.r("ic")
			elif self.ends("ful"):     self.r("")
		elif self.word[self.index] == 's':
			if self.ends("ness"):      self.r("")

	#########################################

	def remove_ant_ence(self):
		if self.word[self.index - 1] == 'a':
			if self.ends("al"): pass
			else: return
		elif self.word[self.index - 1] == 'c':
			if self.ends("ance"): pass
			elif self.ends("ence"): pass
			else: return
		elif self.word[self.index - 1] == 'e':
			if self.ends("er"): pass
			else: return
		elif self.word[self.index - 1] == 'i':
			if self.ends("ic"): pass
			else: return
		elif self.word[self.index - 1] == 'l':
			if self.ends("able"): pass
			elif self.ends("ible"): pass
			else: return
		elif self.word[self.index - 1] == 'n':
			if self.ends("ant"): pass
			elif self.ends("ement"): pass
			elif self.ends("ment"): pass
			elif self.ends("ent"): pass
			else: return
		elif self.word[self.index - 1] == 'o':
			if self.ends("ion") and (self.word[self.offset] == 's' or self.word[self.offset] == 't'): pass
			elif self.ends("ou"): pass
			# takes care of -ous
			else: return
		elif self.word[self.index - 1] == 's':
			if self.ends("ism"): pass
			else: return
		elif self.word[self.index - 1] == 't':
			if self.ends("ate"): pass
			elif self.ends("iti"): pass
			else: return
		elif self.word[self.index - 1] == 'u':
			if self.ends("ous"): pass
			else: return
		elif self.word[self.index - 1] == 'v':
			if self.ends("ive"): pass
			else: return
		elif self.word[self.index - 1] == 'z':
			if self.ends("ize"): pass
			else: return
		else:
			return
		if self.measure() > 1:
			self.index = self.offset

	#########################################

	def remove_final_e_ll(self):
		self.offset = self.index
		if self.word[self.index] == 'e':
			a = self.measure()
			if a > 1 or (a == 1 and not self.cvc(self.index-1)):
				self.index = self.index - 1
		if self.word[self.index] == 'l' and self.double_c(self.index) and self.measure() > 1:
			self.index = self.index -1

	#########################################

	def stem(self, word, last_index, first_index):
		self.word = word
		self.first = last_index
		self.index = first_index
		if self.index <= self.first + 1:
			return self.word 

		self.remove_plurals_ing_ed()
		self.set_y_to_i()
		self.double_suffix_to_single()
		self.remove_full_ness()
		self.remove_ant_ence()
		self.remove_final_e_ll()
		return self.word[self.first:self.index+1]


#############################################