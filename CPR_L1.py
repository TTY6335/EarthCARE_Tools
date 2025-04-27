# coding:utf-8
import numpy as np
from osgeo import gdal,gdalconst
import sys
import tifffile

__author__ = "TTY6335 https://github.com/TTY6335"

if __name__ == '__main__':

########################
#入力するファイルの情報#
########################
	input_data=sys.argv[1]

########################
#出力するファイルの情報#
########################
	output_file=sys.argv[2]

