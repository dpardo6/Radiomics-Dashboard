import SimpleITK as sitk 
import numpy as np
from skimage import exposure
import os

indir=r"C:\Users\pardo\OneDrive\Desktop\AI Lab Play Data\Data\Xrays" #put input dir here
outdir=r"C:\Users\pardo\OneDrive\Desktop\AI Lab Play Data\Data\NewXrays" #specify outputdirhere

for file in os.listdir(indir):
    
    outpath=os.path.join(outdir,file.split('.')[0]+'.png')
    currentimage=sitk.ReadImage(os.path.join(indir,file))
    tarray=sitk.GetArrayFromImage(currentimage)
    narray=exposure.equalize_hist(tarray)
    narray *= 255 
    narray = narray.astype(np.uint8)
    nimage=sitk.GetImageFromArray(narray)
    sitk.WriteImage(nimage,outpath)
