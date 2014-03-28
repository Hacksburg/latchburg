# Latchburg #

## Hacksburg door access system, for use with a Raspberry Pi ##

As a condition of Hacksburg's lease, we were required to implement a
door-access system using magstripe cards like those issued to students and
faculty by the local university (Virginia Tech). This is our fairly simple
solution: We have a raspberry pi connected to a relay that opens and closes the
latch on the door, and a magstripe reader connected as a keyboard device.

When someone swipes their card, the event is read in, the card data is hashed,
and the hash is compared against a list of hashes in an access control file.
If the hash is found in the file, the latch opens for ten seconds. If not,
nothing happens and a log entry is added.

The meet script accepts a card swipe and adds the result to the list of
authorized users.

Both the meet script and the doorman script must be run as root, in an
environment containing python 2.7 and the libraries listed in requirements.txt.
