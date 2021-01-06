
def dicom_to_jpg(n=int, df=object, cfg=[]):
  
  ''' This function iterates over a dataframe of image metadata and converts
  the file types from dicom to JPG. It takes a metadata dataframe, the number of
  images to be processed and the views to be included (Extracted from config.yml).  
  

  Requirements
  ------------

  pydicom==1.4.2

  Parameters
  ------------

  n: int
    number of images to process 
  df: object
    dataframe containing the metadata for the images to be processed.
  cfg: configuration settings
    Extracted from config.yml. includes the image views to be included.
  
  Returns
  ------------

  A dataframe object with n instances of metadata for images converted to jpg from
  the rsna dataset.

  '''

  
  try:
    import pydicom as dicom
  except: 
    !pip install pydicom==1.4.2
    import pydicom as dicom
  import os
  import cv2

  counter = 0
  idxs = []

  for df_idx in df.index.values.tolist():
    filename = df.loc[df_idx]['patientId']
    ds = dicom.dcmread(os.path.join(rsna + 'stage_2_train_images/' + filename + '.dcm'))
    if any(view in ds.SeriesDescription.split(' ')[1] for view in cfg['IMAGES']['VIEWS']):
      if not os.path.exists(rsna + filename + '.jpg'):
        cv2.imwrite(os.path.join(rsna + filename + '.jpg'), ds.pixel_array)
      idxs.append(df_idx)
      counter += 1
    if counter >= n:
      break
  df = df.loc[idxs]
  print(counter,' images were converted.')

  return df