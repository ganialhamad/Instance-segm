import os
import cv2

dirs = os.listdir()
x_folder = os.path.join(dirs, 'supply')

for idx, folder in dirs if dirs.include('lists_of_x'):
  print('000x', idx, folder)
  for idx, file in x_folder if x_folder.isDir():
    if file == 'xos':
      print('x000', idx, file)
      cv2.readim(file, '.jpg')
