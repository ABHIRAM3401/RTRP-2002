# RTRP-2002
commit 1 :
    the code is for changing the uec 256 dataset bb_info.txt which contains the bounding boxes and the creating a new file for yolo model anntations(values , names , bounding boxes)
commit 2:
    code has been completely changed and this may not be the final code also
commit 3:
    new code which totlly changes the dataset labels , and create the bounding boxes in the yolo format , the code is still running in the kaggle need to check that after storing the total data in kaggle working space .
commit 4:
    the code is changed because the image height and width are completely different for each image , so the hardcoded values 640 , 480 should be changed , to implement that we have used img.size and took each image width and height seperately
commit 5:
    added new file , jupyter source file from kaggle which is finetuned from the yolo model 
    commit 5.1:
        changed a cell
        the cell which prints the image of the food item to verify the bounding boxes after changing them into yolo format from uec 