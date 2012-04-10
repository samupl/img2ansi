<h1>img2ansi</h1>

<h2>Description</h2>
<p>Just a simple img to ansi converter. It can be used to create such console "graphics" like this one that I have used in <a href="https://github.com/samaelszafran/bsdinfo">bsdinfo</a>.</p>

<h2>Requirements</h2>
<p>I'm not sure which versions are actually required, but for sure you need to have these packages:</p>

<ul>
	<li>Python 2</li>
	<li>Python module: Image</li>
	<li>Python module: bisect</li>
	<li>Python module: random</li>
</ul>

<h2>Usage</h2>

<pre>
syntax: img2ansi.py <image> <width> <height> [<options...>]
 
options can be one of the following:
 
ansichar=...    - the character used as the foreground of the output.
                  ignored when ascii is set to true (default: 0)
ansipalette=... - the palette of ascii characters that will be used
                  if ansichar=random.
ascii=...       - if set to true, the luminosity will be represented by
                  a ascii character with a similar 'optical weight'.
bgcolor=...     - HEX representation of a color (without the leading '#'
                  that will be transparent in the output (replaced by a
                  a whitespace.
echo=...        - if set to true, the output will converted to a string
                  which can be copied into other print/echo commands.
randomansi=...  - will use a random character from ansipalette, instead
                  of the ansichar value
revert=...      - if set to true, the greyscale charset collection will
                  be reverted (might look better on brighter images.
 
</pre>
