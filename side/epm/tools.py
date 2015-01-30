from __future__ import with_statement

import os
import sys
import codecs
from side import settings

import logging
logger = logging.getLogger(__name__)

sourceFormats = ['gb2312', 'ascii', 'utf-16']
targetFormat = 'utf-8'
outputDir = settings.MEDIA_ROOT + 'converted/temp.csv'


def convertFile(fileName):
    for format in sourceFormats:
        try:
            with codecs.open(fileName, 'rU', 'utf-16') as sourceFile:
                logger.debug("format is:" + format)
                writeConversion(sourceFile)
                logger.debug('Done.')
                return
        except UnicodeDecodeError:
            pass

    logger.debug("Error: failed to convert '" + fileName + "'.")


def writeConversion(fileName):
    with codecs.open(outputDir, 'w', targetFormat) as targetFile:
        for line in fileName:
            targetFile.write(line)
