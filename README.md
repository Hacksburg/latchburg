latchburg
=========

Hacksburg door access system, for use with a Raspberry Pi.

Basically, we were required to implement a door-access system using magstripe
cards like those the local university (Virginia Tech) issues to students and
faculty. This is our fairly simple solution: We have a raspberry pi connected
to a relay that opens and closes the door, and a magstripe reader connected
as a keyboard device.

When someone swipes their card, the event is read in, the card data is hashed,
and the hash is compared against a list of hashes in an access control file.
If the hash is found in the file, the latch opens for ten seconds. If not,
nothing happens and a log entry is added.
