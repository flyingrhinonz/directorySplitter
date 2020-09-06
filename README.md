directorySplitter
=================

Copyright (C) 2020 Kenneth Aaron.

flyingrhino AT orcon DOT net DOT nz

Freedom makes a better world: released under GNU GPLv3.

https://www.gnu.org/licenses/gpl-3.0.en.html

This software can be used by anyone at no cost, however if you like using my software and can support - please donate money to a children's hospital of your choice.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation: GNU GPLv3. You must include this entire text with your distribution.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

Installing:
Download the script and give it execute permissions.

Use './directorySplitter.py -h' for help

Copies files from source directories to destination directory under the same name as the source directory. Use the -f flag to specify how many files will be in each target subdirectory (default 250). Subdirs are suffixed with '_n' where n increments as more directories are required.
If more than 9 subdirs are required, it becomes nn and if more than 99 then nnn and so on.

The reason I wrote this is that my car stereo has a limit of 256 files per directory, and my source directories have significantly more files than that.
I'm sure you'll find more uses for it!

Example: ./directorySplitter.py -f 200 -t /media/ken/1456-C776/ -s /tmp/dir1/ /tmp/dir2/ /tmp/dir3/

Troubleshooting:
Increase the logging verbosity to /var/log/syslog by changing this value in the script:
LogWrite.setLevel(logging.DEBUG)

