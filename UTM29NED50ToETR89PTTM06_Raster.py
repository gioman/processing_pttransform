# -*- coding: latin-1 -*-

"""
***************************************************************************
    UTM29NED50ToETR89PTTM06_Raster.py
    ---------------------
    Date                 : July 2014
    Copyright            : (C) 2014 by Pedro Ven�ncio, Giovanni Manghi
    Email                : pedrongvenancio at gmail dot com
                           giovanni dot manghi at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Pedro Ven�ncio, Giovanni Manghi'
__date__ = 'July 2014'
__copyright__ = '(C) 2014, Pedro Ven�ncio, Giovanni Manghi'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import inspect
import os

from PyQt4.QtGui import *

from qgis.core import *

from processing.gui.Help2Html import getHtmlFromRstFile

try:
    from processing.parameters.ParameterRaster import ParameterRaster
    from processing.outputs.OutputRaster import OutputRaster
except:
    from processing.core.parameters import ParameterRaster
    from processing.core.outputs import OutputRaster

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils


class UTM29NED50ToETR89PTTM06_Raster(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/pttransform.svg')

    def help(self):
        name = self.commandLineName().split(':')[1].lower()
        filename = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'help', name + '.rst')
        try:
          html = getHtmlFromRstFile(filename)
          return True, html
        except:
          return False, None

    def defineCharacteristics(self):
        self.name = 'De UTM 29N ED50 para PT-TM06/ETRS89 Raster'
        self.group = 'Transforma��o de Datum em Rasters'
        self.addParameter(ParameterRaster(self.INPUT, 'Ficheiro de Entrada', False))
        self.addOutput(OutputRaster(self.OUTPUT, 'Ficheiro de Sa�da'))

    def processAlgorithm(self, progress):
        arguments = ['-s_srs',
                     '+proj=utm +zone=29 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/ptED_e89.gsb +wktext +units=m +no_defs',
                     '-t_srs',
                     'EPSG:3763',
                     '-r',
                     'bilinear',
                     '-dstnodata',
                     'nan'
                    ]
        arguments.append('-of')
        out = self.getOutputValue(self.OUTPUT)
        arguments.append(GdalUtils.getFormatShortNameFromFilename(out))
        arguments.append(self.getParameterValue(self.INPUT))
        arguments.append(out)

        GdalUtils.runGdal(['gdalwarp', GdalUtils.escapeAndJoin(arguments)],
                          progress)
