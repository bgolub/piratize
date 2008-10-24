"""
Talk like a Pirate.

Originally in PHP as part of Dougal Campbell's Text Filter Suite
(http://dougal.gunters.org/blog/2004/08/30/text-filter-suite), and ported to
Python by Jacob Kaplan-Moss (jacob@jacobian.org). You'll be able to find
updates, if there are any, at http://toys.jacobian.org/misc/pirate.py.txt.

Licensed, as the original is, under the GPL:
http://www.fsf.org/licensing/licenses/gpl.html. Hooray for license lock-in.
"""

import re
import random
from functools import partial

# Public API ##################################################################

def pirate(content):
    return CDATA_PATTERN.sub(pirate_filter, content)

# The rest be private-ish. Arr. ###############################################
    
def pirate_filter(m):
    bit = m.group(0)
    for pat, repl in PIRATE_PATTERNS:
        bit = pat.sub(repl, bit)
    return bit

def avast(m, chance):
    if random.randint(0, chance) == chance:
        return random.choice(SHOUTS) % {"stub": m.group(0)}
    else:
        return m.group(0)

CDATA_PATTERN = re.compile("(?:(?<=>)|\A)([^<>]+)(?:(?=<)|\Z)")
PIRATE_PATTERNS = [(re.compile(p, re.I), r) for (p,r) in [
    (r'\bmy\b', 'me'),
    (r'\bboss\b', 'admiral'),
    (r'\bmanager\b', 'admiral'),
    (r'\b[Cc]aptain\b', "Cap'n"),
    (r'\bmyself\b', 'meself'),
    (r'\byour\b', 'yer'),
    (r'\byou\b', 'ye'),
    (r'\bfriend\b', 'matey'),
    (r'\bfriends\b', 'maties'),
    (r'\bco[-]?worker\b', 'shipmate'),
    (r'\bco[-]?workers\b', 'shipmates'),
    (r'\bpeople\b', 'scallywags'),
    (r'\bearlier\b', 'afore'),
    (r'\bold\b', 'auld'),
    (r'\bthe\b', "th'"),
    (r'\bof\b',  "o'"),
    (r"\bdon't\b%", "dern't"),
    (r'\bdo not\b', "dern't"),
    (r'\bnever\b', "ne'er"),
    (r'\bever\b', "e'er"),
    (r'\bover\b', "o'er"),
    (r'\bYes\b', 'Aye'),
    (r'\bNo\b', 'Nay'),
    (r'\bYeah\b', 'Aye'),
    (r'\byeah\b', 'aye'),
    (r"\bdon't know\b%", "dinna"),
    (r"\bdidn't know\b%", "did nay know"),
    (r"\bhadn't\b%", "ha'nae"),
    (r"\bdidn't\b%", "di'nae"),
    (r"\bwasn't\b%", "weren't"),
    (r"\bhaven't\b%", "ha'nae"),
    (r'\bfor\b', 'fer'),
    (r'\bbetween\b', 'betwixt'),
    (r'\baround\b', "aroun'"),
    (r'\bto\b', "t'"),
    (r"\bit's\b%", "'tis"),
    (r'\bwoman\b', 'wench'),
    (r'\bwomen\b', 'wenches'),
    (r'\blady\b', 'wench'),
    (r'\bwife\b', 'lady'),
    (r'\bgirl\b', 'lass'),
    (r'\bgirls\b', 'lassies'),
    (r'\bguy\b', 'lubber'),
    (r'\bman\b', 'lubber'),
    (r'\bfellow\b', 'lubber'),
    (r'\bdude\b', 'lubber'),
    (r'\bboy\b', 'lad'),
    (r'\bboys\b', 'laddies'),
    (r'\bchildren\b', 'little sandcrabs'),
    (r'\bkids\b', 'minnows'),
    (r'\bhim\b', 'that scurvey dog'),
    (r'\bher\b', 'that comely wench'),
    (r'\bhim\.\b', 'that drunken sailor'),
    (r'\bHe\b', 'The ornery cuss'),
    (r'\bShe\b', 'The winsome lass'),
    (r"\bhe's\b%", 'he be'),
    (r"\bshe's\b%", 'she be'),
    (r'\bwas\b', "were bein'"),
    (r'\bHey\b', 'Avast'),
    (r'\bher\.\b', 'that lovely lass'),
    (r'\bfood\b', 'chow'),
    (r'\bmoney\b', 'dubloons'),
    (r'\bdollars\b', 'pieces of eight'),
    (r'\bcents\b', 'shillings'),
    (r'\broad\b', 'sea'),
    (r'\broads\b', 'seas'),
    (r'\bstreet\b', 'river'),
    (r'\bstreets\b', 'rivers'),
    (r'\bhighway\b', 'ocean'),
    (r'\bhighways\b', 'oceans'),
    (r'\binterstate\b', 'high sea'),
    (r'\bprobably\b', 'likely'),
    (r'\bidea\b', 'notion'),
    (r'\bcar\b', 'boat'),
    (r'\bcars\b', 'boats'),
    (r'\btruck\b', 'schooner'),
    (r'\btrucks\b', 'schooners'),
    (r'\bSUV\b', 'ship'),
    (r'\bairplane\b', 'flying machine'),
    (r'\bjet\b', 'flying machine'),
    (r'\bmachine\b', 'contraption'),
    (r'\bdriving\b', 'sailing'),
    (r'\bunderstand\b', 'reckon'),
    (r'\bdrive\b', 'sail'),
    (r'\bdied\b', 'snuffed it'),
    (r'ing\b/', "in'"),
    (r'ings\b/', "in's"),
    (r'(\.\s)', partial(avast, chance=3)),
    (r'([!\?]\s)', partial(avast, chance=2)),
]]

SHOUTS = [
    ", avast%(stub)s",
    "%(stub)s Ahoy!",
    ", and a bottle of rum!",
    ", by Blackbeard's sword%(stub)s",
    ", by Davy Jones' locker%(stub)s",
    "%(stub)s Walk the plank!",
    "%(stub)s Aarrr!",
    "%(stub)s Yaaarrrrr!",
    ", pass the grog!",
    ", and dinna spare the whip!",
    ", with a chest full of booty%(stub)s",
    ", and a bucket o' chum%(stub)s",
    ", we'll keel-haul ye!",
    "%(stub)s Shiver me timbers!",
    "%(stub)s And hoist the mainsail!",
    "%(stub)s And swab the deck!",
    ", ye scurvey dog%(stub)s",
    "%(stub)s Fire the cannons!",
    ", to be sure%(stub)s",
    ", I'll warrant ye%(stub)s",
    ", on a dead man's chest!",
    "%(stub)s Load the cannons!",
    "%(stub)s Prepare to be boarded!",
    ", I'll warrant ye%(stub)s",
    "%(stub)s Ye'll be sleepin' with the fishes!",
    "%(stub)s The sharks will eat well tonight!",
    "%(stub)s Oho!",
    "%(stub)s Fetch me spyglass!",
]

if __name__ == '__main__':
    import sys
    for line in sys.stdin:
        sys.stdout.write(pirate(line))