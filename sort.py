import os,shutil
folders={
    'videos':['.mp4'],
    'audios':['.wav','.mp3'],
    'images':['.jpg','.png'],
    'documents':['.doc','.xlsx','.xls','.pdf','.zip','.rar'],
}
directory=input("Enter the location : ")
all_files=os.listdir(directory)
#print(all_files) C:\Users\91858\Downloads\project IMS
for i in all_files:
    if os.path.isfile(directory + "\\" +i)==True:
        print("yes")