#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of tools for Unicode-encoded text processing.

Date: Jan, 2014
Author: Duy K. Ninh
Tested under Python 2.7
"""

# Built-in modules
import unicodedata

###############################################################
#	List of diacritics and tone of Vietnamse alphabet:
#           + Diacritic     Explanation
#             	'*'	    	u* = ư, o* = ơ			
#	      		'^'	    	a^ = â, e^ = ê, o^ = ô
#	      		'<'	    	a< = ă
#	      		'~'	    	d~ = đ		
#           + Tone          VN name (EN name)
#	      		'_1'	    ngang   (level)
#	      		'_2'	    huyền   (grave)
#	      		'_3'	    ngã	    (tilde)
#	      		'_4'	    hỏi     (hook above)
#             	'_5'	    sắc     (acute)
#             	'_6'	    nặng    (dot below)
#
###############################################################


######################
# Module's functions #
######################

		
def CompUnicode2Unicode(text, f):
	"""
	Convert from Composite Unicode to UTF-8 Unicode for a Vietnamese text.
	
	Input parameters:
		- text	: text in both UTF-8 Unicode and Composite Unicode
		- f 	: file handle of the Unicode conversion data file
	Return value:
		- text 	: text in UTF-8 Unicode
	"""
	
	# load a dict. of comp. Unicode to UTF-8 Unicode maps
	cu2u = {}
	
	for line in f:
		chars = line.split()
		if len(chars) > 2: continue
		cu2u[chars[0]] = chars[1]
	
	# replace any comp. Unicode char with the corr. UTF-8 Unicode one		
	for k in cu2u.keys():			
		text = text.replace(k, cu2u[k])
		
	return text
		
	
def DetectLettersAndTone(text):
	"""
	DetectLettersAndTone(text) -> list of letters and tone
	
	Return a list of strings comprising letters and tone from a Unicode-encoded text of a syllable.
	Only one tone is returned at the end of the list if text has at least a letter.
	Otherwise, the tone is returned as an empty string.
	
	>>> DetectLettersAndTone(u'Quy\u1ec1n')	#'Quyền'
	['Q', 'u', 'y', 'e^', 'n', '_2']
	>>> DetectLettersAndTone(u'Qu\u1eb3ng') #'Quẳng'
	['Q', 'u', 'a<', 'n', 'g', '_4']
	"""
	
	# initialize
	letters = []
	tone = '_1'	# ngang (default tone)
	bHasLetter = False
	
	# process every character
	for char in text:
		# get Unicode character's properties
		try:
			char_name = unicodedata.name(char)
			#print char_name
		except:
			char_name = ''		
		
		# get base letter
		if 'LETTER' in char_name:
			bHasLetter = True
			lett = char_name[char_name.index('LETTER') + 7]
			if 'SMALL' in char_name:
				lett = lett.lower()
		
			# detect diacritic
			if 'HORN' 		in char_name: 	lett += '*'	# for ư, ơ			
			if 'CIRCUMFLEX' in char_name: 	lett += '^'	# for â, ê, ô 
			if 'BREVE' 		in char_name: 	lett += '<'	# for ă
			if 'STROKE' 	in char_name: 	lett += '~'	# for đ		
			
			# detect tone
			if 'GRAVE' 		in char_name: 	tone = '_2'	# huyền
			if 'TILDE' 		in char_name: 	tone = '_3'	# ngã		
			if 'HOOK ABOVE'	in char_name: 	tone = '_4'	# hỏi
			if 'ACUTE'		in char_name: 	tone = '_5'	# sắc
			if 'DOT BELOW'	in char_name: 	tone = '_6'	# nặng
		else:
			lett = char
	
		# append letter to result list	
		letters.append(lett)
	
	# finally, append tone to result list
	if bHasLetter:	letters.append(tone)
	else:		letters.append('')
	
	return letters


def IsSpecialChar(char):
	"""
	Check if a character is a typeable punctuation/ellipsis/sign/mark/superscript/subscript.
	"""
	
	PUNC 	 = '/\[]{}#$@,;\"\'%():`&!?+-*_^~|.'	# typeable punctuations
	
	if char in PUNC: return True
	try:
		char_name = unicodedata.name(char)
	except:
		char_name = ''
		
	if ('ELLIPSIS' in char_name) or ('DASH' in char_name) \
		or ('SIGN' in char_name) or ('MARK' in char_name) \
		or ('SUPERSCRIPT' in char_name) or ('SUBSCRIPT' in char_name): return True
	return False


def _test():
	import doctest
	return doctest.testmod()
	
if __name__ == '__main__':
	_test()