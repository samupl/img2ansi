#!/usr/bin/env python
# -*- encoding: utf-8 -*

#
#   Copyright (c) 2011 Jakub Szafrański <samu@pirc.pl>
# 
#  All rights reserved.
# 
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
# 
#  THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
#  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#  SUCH DAMAGE.
#
import sys
import Image
import rgb256
import random

def tohex((r,g,b)):
    hexchars = "0123456789ABCDEF"
    return hexchars[r/16]+hexchars[r%16]+hexchars[g/16]+hexchars[g%16]+hexchars[b/16]+hexchars[b%16]

cprefix = "\033"

#
# Defaults. These can be modified by commandline options.
#

_o = {}
_o['o_echo'] = 0
_o['bgcolor'] = "0"
_o['ansichar'] = "0"
_o['ascii'] = "false"
_o['randomansi'] = "false"
_o['revert'] = "false"
_o['echo'] = "false"
_o['ansipalette'] = ".,-_ivc=!/|\\~gjez2]/(YL)t[+T7VfmdK4ZGbNDXY5P*QW8KMA""#%$"

for e in sys.argv:        
    try:
        e = e.split("=")
        #print e
        if e[0] in _o:
            _o[e[0]] = e[1]
    except:
        pass
        
_o['bgcolor'] = _o['bgcolor'].upper()
_o['ascii'] = _o['ascii'].upper()
_o['revert'] = _o['revert'].upper()
_o['echo'] = _o['echo'].upper()
_o['randomansi'] = _o['randomansi'].upper()

if _o['echo'] == "TRUE":
    cprefix="\\033"
    
try:
    img = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
except:
    print "%s: Wrong # of args!" % sys.argv[0]
    print "syntax: %s <image> <width> <height> [<options...>]" % sys.argv[0]
    print " "
    print "options can be one of the following:"
    print " "
    print "ansichar=...    - the character used as the foreground of the output."
    print "                  ignored when ascii is set to true (default: 0)"
    print "ansipalette=... - the palette of ascii characters that will be used"
    print "                  if ansichar=random."
    print "ascii=...       - if set to true, the luminosity will be represented by"
    print "                  a ascii character with a similar 'optical weight'."
    print "bgcolor=...     - HEX representation of a color (without the leading '#'"
    print "                  that will be transparent in the output (replaced by a"
    print "                  a whitespace."
    print "echo=...        - if set to true, the output will converted to a string"
    print "                  which can be copied into other print/echo commands."
    print "randomansi=...  - will use a random character from ansipalette, instead"
    print "                  of the ansichar value"
    print "revert=...      - if set to true, the greyscale charset collection will"
    print "                  be reverted (might look better on brighter images."
    print " "
    exit(1)



try:
    im = Image.open(sys.argv[1])
except:
    print "Error while opening file %s" % sys.argv[1]

im = im.resize((width, height), Image.BILINEAR)

    
if _o['ascii'] == "TRUE":
    from bisect import bisect
    greyscale = [
                " ",
                " ",
                ".,-",
                "_ivc=!/|\\~",
                "gjez2]/(YL)t[+T7Vf",
                "mdK4ZGbNDXY5P*Q",
                "W8KMA",
                "#%$"
                ]
    zonebounds=[36,72,108,144,180,216,252]
    im2 = Image.open(sys.argv[1])
    im2 = im2.resize((width, height), Image.BILINEAR)
    im2 = im2.convert("L")

if _o['revert'] == "TRUE":
    greyscale.reverse()


for y in range(0, im.size[1]):
    line = ""
    for x in range(0, im.size[0]):
        hexcolor = tohex(im.getpixel( (x,y) ))
        if (hexcolor != _o['bgcolor']):
            if _o['randomansi'] == "TRUE":  
                _o['ansichar'] = _o['ansipalette'][random.randint(0,len(_o['ansipalette'])-1)]
            color = str(rgb256.rgb_to_256(hexcolor)).strip()
            if _o['ascii'] == 'TRUE':
                lum = 255 - im2.getpixel((x,y))
                row = bisect(zonebounds,lum)
                possibles = greyscale[row]
                _o['ansichar'] = possibles[random.randint(0,len(possibles)-1)]
            line += cprefix+"[38;5;"+color+"m"+_o['ansichar']+cprefix+"0;0;0m"
        else:
            line += " "
    print line
