#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of tools for letter-to-sound conversion.

Date: Jan, 2014
Author: Duy K. Ninh
Tested under Python 2.7
"""

###############################################################
#   List of diacritics and tone of Vietnamse alphabet:
#           + Diacritic     Explanation
#               '*'         u* = ư, o* = ơ          
#               '^'         a^ = â, e^ = ê, o^ = ô
#               '<'         a< = ă
#               '~'         d~ = đ      
#           + Tone          VN name (EN name)
#               '_1'        ngang   (level)
#               '_2'        huyền   (grave)
#               '_3'        ngã     (tilde)
#               '_4'        hỏi     (hook above)
#               '_5'        sắc     (acute)
#               '_6'        nặng    (dot below)
#
###############################################################

#################
# Module's data #
#################

STOP_SNDS   = ['p','t','k'] # stop consonants as a coda
MAX_CODA_LEN    = 2     # maximum number of alphabet letters for a coda
MAX_NUCL_LEN    = 2     # maximum number of alphabet letters for a nucleus
SPECIAL_GI_LST  = ['gie^ng','gic','gin','gie^m','gie^t','gi'] # list of base syllables has pattern '^gi' but letter 'i' is included in the nucleus

##### Vietnamese letter-to-sound (L2S) rules defined according to the sound's position in a syllable
##### Format of each mapping: {letter: sound in TUPS symbols}
# Initinal's L2S mappings
init_l2s_maps = \
        [{'m'   : 'm'   },
        {'n'    : 'n'   },
        {'nh'   : 'nj'  },
        {'ng'   : 'N'   },
        {'ngh'  : 'N'   },
        {'b'    : 'b'   },
        {'p'    : 'p'   },
        {'d~'   : 'd'   },
        {'t'    : 't'   },
        {'th'   : 'tH'  },
        {'tr'   : 'tr'  },
        {'ch'   : 'c'   },
        {'c'    : 'k'   },
        {'k'    : 'k'   },
        {'q'    : 'k'   },
        {'v'    : 'v'   },
        {'ph'   : 'f'   },
        {'d'    : 'z'   },
        {'gi'   : 'z'   },
        {'x'    : 's'   },
        {'r'    : 'zr'  },
        {'s'    : 'sr'  },
        {'g'    : 'G'   },
        {'gh'   : 'G'   },
        {'kh'   : 'x'   },
        {'h'    : 'h'   },
        {'l'    : 'l'   },  
        {''     : 'Q'   }]
# Onset's L2S mappings
onst_l2s_maps = \
        [{'u'   : 'w'   },
        {'o'    : 'w'   },
        {''     : ''    }]
# Coda's L2S mappings
coda_l2s_maps = \
        [{'m'   : 'm'   },
        {'n'    : 'n'   },
        {'ng'   : 'N'   },
        {'nh'   : 'N'   },
        {'p'    : 'p'   },
        {'t'    : 't'   },
        {'c'    : 'k'   },
        {'ch'   : 'k'   },
        {'i'    : 'ji'  },
        {'y'    : 'ji'  },
        {'o'    : 'wu'  },
        {'u'    : 'wu'  },
        {''     : ''    }]
# Nucleus's L2S mappings
nucl_l2s_maps = \
        [{'u'   : 'u'   },
        {'u*'   : 'W'   },
        {'o^'   : 'o'   },
        {'o*'   : 'oU'  },
        {'a^'   : 'oUs' },
        {'oo'   : 'O'   },
        {'i'    : 'i'   },
        {'y'    : 'i'   },
        {'e^'   : 'e'   },
        {'e'    : 'E'   },
        {'a<'   : 'as'  },
        {'ie^'  : 'ie'  },
        {'ia'   : 'ie'  },
        {'ye^'  : 'ie'  },
        {'ya'   : 'ie'  },
        {'uo^'  : 'uo'  },
        {'ua'   : 'uo'  },
        {'u*o*' : 'WoU' },
        {'u*a'  : 'WoU' },
        {'o'    : ['O','Os']},
        {'a'    : ['Es','a','as']}]
##### Notes:
# L2S rules for letters 'o' & 'a' are more complex to resolve ambiguities as follows:
#   - For 'o':
#       {'o'    : 'Os'  } if the syllable follows the pattern 'ong$' or 'oc$'
#       {'o'    : 'O'   } in other cases
#   - For 'a':
#       {'a'    : 'Es'  } if the syllable follows the pattern 'anh$' or 'ach$'
#       {'a'    : 'as'  } in the syllable follows the pattern 'ay$' or 'au$'
#       {'a'    : 'a'   } in other cases

init_letters = [list(d)[0] for d in init_l2s_maps] # letter list for the initial
onst_letters = [list(d)[0] for d in onst_l2s_maps] # letter list for the onset
nucl_letters = [list(d)[0] for d in nucl_l2s_maps] # letter list for the nucleus
coda_letters = [list(d)[0] for d in coda_l2s_maps] # letter list for the coda


######################
# Module's functions #
######################

def _SearchBackSylComp(let_seq, max_len, comp_let_lst):
    """
    Return the longest letter sequence that acts as a specified syllable component and its number of letters.
    The search is performed from right-to-left on input letter sequence.
    """
    # maximum number of letters to try searching
    num = min(max_len, len(let_seq))
    while num > 0:
        s = ''
        for i in range(-num,0): s += let_seq[i]
        if s in comp_let_lst: break
        num -= 1
    if num == 0: s = ''
    return (s, num)


def ConvertLettersToSounds(letters_tone, nTones=8):
    """
    ConvertLettersToSounds(letters_tone, nTones=8) -> list of sounds.   
    Return a list of phones from a list of letters and tone of a syllable
    or an empty list if the syllable is unpronounceable.
    
    Input parameters:
        - letters_tone  : list of letters and tone
        - nTones        : number of tones (6 for official set, 8 for extended set (default))
    Return value:
        - sounds        : list of phones
    
    >>> ConvertLettersToSounds(['Q','u','y','e^','n','_2'])
    ['k', 'w', 'ie', 'n', '_2']
    >>> ConvertLettersToSounds(['q','u','y','e^','t','_5'])
    ['k', 'w', 'ie', 't', '_7']
    >>> ConvertLettersToSounds(['A','p','p','l','e','_1'])
    []
    """
    
    # initialize
    letters = [l.lower() for l in letters_tone[:-1]]    # lowerized letter list
    base_syl = ''.join(letters) # base syllable (without tone) in string    
    tone = letters_tone[-1]     # tone  
    left_bound = -1             # index of the right-most processed letter from the left
    right_bound = len(letters)  # index of the left-most processed letter from the right
    onst_let = ''               # empty onset
    
    ##### process the initial
    # search forward the longest letter sequence for the initial (if any)
    init_let = ''
    while (init_let + letters[left_bound + 1]) in init_letters:
        left_bound += 1
        init_let += letters[left_bound]
        if left_bound + 1 == right_bound: break
    
    # then, convert initial letter to sound
    idx = init_letters.index(init_let)
    init_snd = list(init_l2s_maps[idx].values())[0]
    
    # special treatments if either of letters 'gi' or 'q' is the initial
    if (init_let == 'gi') and (base_syl in SPECIAL_GI_LST):
        left_bound = 0  # letter 'i' is included in the nucleus, e.g., 'gie^ng'
    if init_let == 'q':     
        onst_let = 'u'  # letter 'u' is always the onset after the initial 'q'
        left_bound = 1
    
    ##### process the coda & the nucleus
    # search backward the longest letter sequence for the coda (if any)
    (coda_let, coda_len) = _SearchBackSylComp(letters[left_bound+1:right_bound], MAX_CODA_LEN, coda_letters)
    tmp_right_bound = right_bound - coda_len    
    
    # search backward the longest letter sequence for the nucleus, given the potential coda
    (nucl_let, nucl_len) = _SearchBackSylComp(letters[left_bound+1:tmp_right_bound], MAX_NUCL_LEN, nucl_letters)
    
    # check if the found coda (if any) is valid
    bValid = False
    if coda_let in 'iyou':      
        if (nucl_len > 0) and (not base_syl.endswith('uy')):
            bValid = True
        else:
            # syllable has no coda --> re-assign coda & nucleus
            nucl_let = coda_let
            coda_let = ''
            right_bound -= coda_len
    else:
        bValid = True   
    if bValid:
        right_bound -= coda_len + nucl_len
    
    # convert coda letter to sound
    idx = coda_letters.index(coda_let)
    coda_snd = list(coda_l2s_maps[idx].values())[0]
    
    # convert nucleus letter to sound
    if nucl_let == '':  # nucleus cannot be found
        return []   
    if nucl_let not in 'oa':
        idx = nucl_letters.index(nucl_let)
        nucl_snd = list(nucl_l2s_maps[idx].values())[0]
    if nucl_let == 'o':
        if base_syl.endswith('ong') or base_syl.endswith('oc'):
                nucl_snd = 'Os'
        else:
                nucl_snd = 'O'
    if nucl_let == 'a':
        if base_syl.endswith('anh') or base_syl.endswith('ach'):
                nucl_snd = 'Es'
        else:
            if base_syl.endswith('ay') or base_syl.endswith('au'):
                nucl_snd = 'as'
            else:
                nucl_snd = 'a'
    
    ##### process the onset
    if left_bound + 1 < right_bound - 1:    # more than one letter left unprocessed
        return []
    elif left_bound + 1 == right_bound - 1: # one letter left unprocessed
        if onst_let != '':
            return []
        elif letters[left_bound + 1] not in onst_letters:
            return []
        else:
            onst_let = letters[left_bound + 1]
        
    # convert onset letter to sound
    idx = onst_letters.index(onst_let)
    onst_snd = list(onst_l2s_maps[idx].values())[0]
    
    ##### refine tones 5 & 6 for closure coda
    if nTones == 8:
        if coda_snd in STOP_SNDS:
            if tone == '_5': tone = '_7'
            if tone == '_6': tone = '_8'
    
    sounds = [init_snd]
    if onst_snd: sounds.append(onst_snd)
    sounds.append(nucl_snd)
    if coda_snd: sounds.append(coda_snd)
    sounds.append(tone)
    return sounds


def _test():
    import doctest
    return doctest.testmod()
    
if __name__ == '__main__':
    _test()