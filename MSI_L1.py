# coding:utf-8
import numpy as np
np.set_printoptions(threshold=100000)
from osgeo import gdal,gdalconst
import sys
import h5py
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
	# band 0: VIS
	# band 1: NIR
	# band 2: SWIR-1
	# band 3: SWIR-2 
	# band 4: TIR Band 7
	# band 5: TIR Band 8
	# band 6: TIR Band 9
	band=int(sys.argv[2])

########################
#出力するファイルの情報#
########################
	output_file=sys.argv[3]

	#hdf5のファイルを開く
	f=h5py.File(input_data,'r')

	lat_arr_1=np.array(f['ScienceData']['latitude'][band],dtype='float64')
	lon_arr_1=np.array(f['ScienceData']['longitude'][band],dtype='float64')
	
	image_data=np.array(f['ScienceData']['pixel_values'][band],dtype='float32')

	#GCPのリストを作る
	gcp_list=[]

	image_max_value=9.9692099683868690e+36

	#両端12ピクセルが余白として設定されているので削る
	lat_arr_1=lat_arr_1[:, 12:-12]
	lon_arr_1=lon_arr_1[:, 12:-12]
	image_data=image_data[:, 12:-12]

	#fillvalueをnanに変換する。
	image_data=np.where(image_data==image_max_value,np.nan,image_data)

	for column in range(0,lat_arr_1.shape[0],200):
		for row in range(0,lat_arr_1.shape[1],50): 
			gcp=gdal.GCP(lon_arr_1[column][row],lat_arr_1[column][row],0,row,column)
			gcp_list.append(gcp)

	for row in range(0,lat_arr_1.shape[1],50): 
		gcp=gdal.GCP(lon_arr_1[-1][row],lat_arr_1[-1][row],0,row,lat_arr_1.shape[0])
		gcp_list.append(gcp)

	#行数
	row_size=image_data.shape[0]
	#列数
	col_size=image_data.shape[1]

	#出力
	dtype = gdal.GDT_Float64
	#バンド数
	band=1
	output = gdal.GetDriverByName('GTiff').Create(output_file,col_size,row_size,band,dtype)
	output.GetRasterBand(1).WriteArray(image_data)
	wkt = output.GetProjection()
	output.SetGCPs(gcp_list,wkt)
	output = gdal.Warp(output_file,\
			output,\
			dstSRS='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs',\
			tps = True,\
			dstNodata=np.nan,\
			outputType=dtype,\
			multithread=True,
			resampleAlg=gdalconst.GRIORA_NearestNeighbour)
	output = None

	f.close()
