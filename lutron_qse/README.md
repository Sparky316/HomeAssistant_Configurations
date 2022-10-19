# Lutron QSE Custom Component
-This works with the Lutron hardware "QSE-CI-NWK-E", referred to as "QS Standalone" in the Lutron docs.

-This is derived from deustis's work here (Big thank you!): https://github.com/deustis/homeassistant-config

-This custom component was created by merging both the telnet interface wrapper and the "cover" portion into a single custom component, as well as some added robustness (in Lutron communication).  

-It seems to be working very well, and snappy.  It auto-finds all roller/cover/shade devices and creates entities for them.  

-Installation: Follow the instructions in ReadMe.txt (Essentially, just install like any Home Assistant custom component)