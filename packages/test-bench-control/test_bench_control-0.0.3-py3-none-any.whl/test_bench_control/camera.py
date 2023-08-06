import os

def take_picture(camera,path,pic_name,libcam_cmd=""):
    
    #################################################################################
    #  Pre:     camera      (integer)   - wich camera should be used D={0,1} 
    #           path        (string)    - path to folder where picture should be
    #           pic_name    (string)    - name and format of picture
    #           libcam_cmd  (string)    - further libcam settings
    #  Post:    no return value
    #  Example: take_picture(0,"/home/raspi/Desktop","my_pic.jpg","--shutter 1000")
    #################################################################################
    
    complete_path=str(path)+"/"+str(pic_name)
    camera_number=str(camera)
    cmd=f"libcamera-jpeg -o {complete_path} --nopreview --camera {camera_number} {libcam_cmd}"
    os.system(cmd)
    
def preview(camera):
    
    #####################################################################
    #  Pre:     camera  (integer)   - wich camera should be used D={0,1}
    #  Post:    no return value
    #  Example: preview(0)
    #####################################################################
    
    camera_number=str(camera)
    cmd=f"libcamera-hello -t 0 --camera {camera_number}"
    os.system(cmd)
