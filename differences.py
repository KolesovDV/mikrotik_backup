import sys
import time

def diff(file_one,file_two):
    try:
     with open(file_one) as text_one, \
            open(file_two) as text_two:
        print(file_one)
        print(file_two)
        
        return set(text_one) ^ set(text_two)
        time.sleep(2)
    except:
        print("can't compare files")
def diff_rsc_files(file_one,file_two,path):
    try:
     with open(path +  '_diff.txt', 'w') as result:
        for i in diff(file_one,file_two):
             result.write(i)
    except:
        print("can't compare files")
