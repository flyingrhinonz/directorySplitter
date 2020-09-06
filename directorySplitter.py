#!/usr/bin/python3

'''
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

'''

# Standard library imports:
import argparse
import atexit
import getpass
import logging
import logging.handlers
import math
import os
import shutil
import sys
import traceback


# This block handles logging to syslog:
LogWrite = logging.getLogger('MyLogger')
LogWrite.setLevel(logging.WARNING)
    # ^ Set this to logging.DEBUG or logging.WARNING for your INITIAL desired log level.
    #   Config file log level takes over from when it is loaded, this value controls
    #   logging verbosity until then.
LogWrite.propagate = False
    # ^ Prevents duplicate logging by ancestor loggers (if any)
LogHandler = logging.handlers.SysLogHandler(address = '/dev/log')
LogWrite.addHandler(LogHandler)
LogWriteFormatter = logging.Formatter('{}: %(message)s'.format('dirSplit'))
    # ^ Appends 'dirSplit' to log lines for easy identification
LogHandler.setFormatter(LogWriteFormatter)


# Global variable declarations go here:
FilesPerDir = 250               # Default maximum number of files per dir. Can be changed via command line arg
SourceDirs = list()             # Source directories to copy
TargetDir = ''                  # Target dir to copy the dirs to


def VerifyDirs():
    global SourceDirs
    global TargetDir
    global FilesPerDir

    if not (os.path.isdir(TargetDir)):
        print('TargetDir={} does not exist. Aborting'.format(TargetDir))
        LogWrite.error('TargetDir={} does not exist. Aborting'.format(TargetDir))
        sys.exit(1)
    else:
        LogWrite.debug('TargetDir={} exists'.format(TargetDir))

    for Looper in SourceDirs:
        if not (os.path.isdir(Looper)):
            print('SourceDir={} does not exist. Aborting'.format(Looper))
            LogWrite.error('SourceDir={} does not exist. Aborting'.format(Looper))
            sys.exit(1)
        else:
            LogWrite.debug('SourceDir={} exists'.format(Looper))

    if TargetDir in SourceDirs:
        print('TargetDir={} cannot be one of the source dirs. Aborting'.format(TargetDir))
        LogWrite.error('TargetDir={} cannot be one of the source dirs. Aborting'.format(TargetDir))
        sys.exit(1)
    else:
        LogWrite.debug('TargetDir={} is not one of the source dirs. This is ok'.format(TargetDir))

    if (FilesPerDir < 1):
        print('FilesPerDir must me >= 1')
        LogWrite.error('FilesPerDir={} must be >= 1. Aborting'.format(FilesPerDir))
        sys.exit(1)


def CopyFiles():
    global FilesPerDir
    global SourceDirs
    global TargetDir

    for SourceDirLooper in SourceDirs:
        SourceDirLooper = SourceDirLooper.rstrip('/')
        FilesList = list()
        DirCounter = 1

        SourceDirName = SourceDirLooper.split('/')[-1]
        LogWrite.debug('Processing: SourceDirName={}'.format(SourceDirName))

        for ListFile in os.listdir(SourceDirLooper):
            FullFilePath = os.path.join(SourceDirLooper, ListFile)
            if os.path.isfile(FullFilePath):
                FilesList.append(FullFilePath)
        FilesList.sort()
        FilesCount = len(FilesList)
        TargetDirCount = math.ceil(FilesCount / FilesPerDir)

        if (TargetDirCount < 10):
            ZfillLength = 1
        elif (TargetDirCount < 100):
            ZfillLength = 2
        elif (TargetDirCount < 1000):
            ZfillLength = 3
        elif (TargetDirCount < 10000):
            ZfillLength = 4
        elif (TargetDirCount < 100000):
            ZfillLength = 5
        elif (TargetDirCount < 1000000):
            ZfillLength = 6
        elif (TargetDirCount < 10000000):
            ZfillLength = 7
        elif (TargetDirCount < 100000000):
            ZfillLength = 8
        elif (TargetDirCount < 1000000000):
            ZfillLength = 9

        LogWrite.debug('SourceDir={} has {} files. Splitting to {} files per dir. '
            'Number of target dirs required: {}. ZfillLength={}'
            .format(SourceDirLooper, FilesCount, FilesPerDir, TargetDirCount, ZfillLength))

        for FileNumber, FileName in enumerate(FilesList, start = 1):
            DirSuffix = os.path.join(TargetDir, str.join('', (SourceDirName, '_', str(DirCounter).zfill(ZfillLength))))
            os.makedirs(DirSuffix, exist_ok = True)
            LogWrite.debug('Created dir: {}'.format(DirSuffix))
            shutil.copy(FileName, DirSuffix)
            LogWrite.debug('Copied file: {}   to: {}'.format(FileName, DirSuffix))
            print('COPIED FILE: {}   TO: {}'.format(FileName, DirSuffix))
            if (int(FileNumber) % FilesPerDir == 0):
                DirCounter += 1

        LogWrite.debug('Copying completed')


# Your function definitions go here:

def ParseArgs():
    global FilesPerDir
    global SourceDirs
    global TargetDir

    parser = argparse.ArgumentParser(
        description='Directory splitter. '
            'This program splits directories into multiple directories with '
            'the specified number of files within each directory.',
        epilog='Thank you for using FlyingRhino software.')
    LogWrite.debug('parser object = "{}"'.format(parser))

    parser.add_argument('-f', '--filesperdir', required = False, type = int, default = FilesPerDir,
        help = 'how many files per directory? Default={}'.format(FilesPerDir))

    parser.add_argument('-s', '--sourcedirs', required = True, nargs = '*',
        help = 'one or more source directories to copy')

    parser.add_argument('-t', '--targetdir', required = True,
        help = 'target directory to put your split dirs')

    args = parser.parse_args()
    LogWrite.debug('args object = "{}"'.format(args))

    if args.filesperdir:
        LogWrite.debug('filesperdir: "{}"'.format(args.filesperdir))
        FilesPerDir = args.filesperdir

    if args.sourcedirs:
        LogWrite.debug('sourcedirs: "{}"'.format(args.sourcedirs))
        SourceDirs = list(args.sourcedirs)

    if args.targetdir:
        LogWrite.debug('targetdir: "{}"'.format(args.targetdir))
        TargetDir = args.targetdir.rstrip()

    LogWrite.debug('FilesPerDir={} , SourceDirs={} , TargetDir={}'
        .format(FilesPerDir, SourceDirs, TargetDir))


# Last function: main(...). Your entry point into the program:
def main(*args):
    ParseArgs()
    VerifyDirs()
    CopyFiles()


# End of functions. main() caller below:

if __name__ == '__main__':
    main()


