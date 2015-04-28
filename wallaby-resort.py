#
# wallaby-move
#
# Created: 2015-04-26
# Author: Ethan Smith
#
# Copyright 2015 Ethan Smith
#


import argparse
from os import listdir, makedirs
from os.path import isdir, join, getmtime, basename, exists, dirname
from time import ctime, strftime, gmtime
import shutil


parser = argparse.ArgumentParser()
parser.add_argument("source", type=str, help="the source directory")
parser.add_argument("destination", type=str, help="the destination directory")
parser.add_argument("-l", "--live", action="store_true", help="move files")
args = parser.parse_args()

def findFiles(rootPath, depth):
   allFiles = [];

   print depthPrefix(depth) + "Looking at: "+rootPath
   # Get all files
   files = listdir(rootPath)

   # Process files
   for filename in files:
      if filename[:1] == '.':
         continue

      fullpath = join(rootPath, filename)

      if isdir(fullpath):
         allFiles = allFiles + findFiles(fullpath, depth+1)
      else:
         allFiles.append(join(rootPath, filename))

   return allFiles;

def depthPrefix(depth):
   return "-" + "-"*(depth*3) + "> ";

def moveFiles(rootPath, files, live):
   for path in files:
      newPath = buildNewPath(rootPath, gmtime(getmtime(path)), basename(path))
      print newPath + " <-------- " + path

      if exists(newPath):
         print "File already exists for source of: " + path;
      elif live:
         directory = dirname(newPath)
         if not exists(directory):
            makedirs(directory)
         shutil.move(path, newPath)

def buildNewPath(rootPath, time, filename):
   return join(baseFolder(time), dateFolder(time), filename)

def baseFolder(time):
   return strftime('%Y', time)

def dateFolder(time):
   return strftime('%Y-%m-%d', time)

files = findFiles(args.source, 0)
moveFiles(args.destination, files, args.live)
