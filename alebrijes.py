import csv
import re
from collections import defaultdict

#SETTING UP VARIABLES - START
score_file_name = "delta_INs_conservation_chainA.csv"
pdb_input_filename = "input.pdb"
#SETTING UP VARIABLES - END


#Uploading conservation score list from the csv file into a list variable "scores_list" - BEGIN
with open(str(score_file_name), 'rb') as f:
    reader = csv.reader(f)
    scores_list = list(reader)

scores_list2 = str(scores_list).split(',') #converting to a list by ',' delimiters
#Uploading conservation score list from the csv file into a list variable "scores_list" - END


#Removing fluff from the list - BEGIN
length = len(scores_list2)

for a in range (0,length):
    print str(scores_list2[a])
    scores_list2[a]=scores_list2[a].replace(' ','')
    scores_list2[a]=scores_list2[a].replace("'",'')
    scores_list2[a]=scores_list2[a].replace(".",'')
    scores_list2[a]=scores_list2[a].replace('11','10')
    scores_list2[a]=re.sub('[^0-9]','',scores_list2[a])

scores_list2 = filter(None,scores_list2) #removes empty strings from list

print str(scores_list2)

length = len(scores_list2)

for a in range (0,length):
    scores_list2[a]=float(scores_list2[a])/10
    scores_list2[a]=str(scores_list2[a]).replace('0.0','') #removes 0.0 values (which are gaps)
    scores_list2[a]=str(scores_list2[a]).replace('1.2','0.0') #changes the 1.2 values into 0.0 indicating a gap in the query sequence, for which a residue in the pdb file exists

scores_list2 = filter(None,scores_list2) #removes empty strings from list

print str(scores_list2)
#Removing fluff from the list - END

#Edit the PDB file line by line - BEGIN
residue_pdb_start = 2
residue_pdb_end = 251
pdb_file=open("input.pdb", "r")
pdb_file_content = pdb_file.read()
pdb_file.close()
number_of_lines = sum(1 for line in open(str(pdb_input_filename)))

print "Number of lines: " + str(number_of_lines)
line_no = 0
all_results=""

for line in range (0, number_of_lines - 1):

    pdb_file2=open(str(pdb_input_filename), "r")
    
    pdb_file_content2 = pdb_file2.readlines()[line]

    pdb_file_content2 = pdb_file_content2.split() #splits the line by whitespace
    
    print "Line number: " + str(line) + "\n" + str(pdb_file_content2)


    if int(pdb_file_content2[5]) > residue_pdb_start-1 and int(pdb_file_content2[5]) < residue_pdb_end + 1:

        pdb_file_content2[10]=str(scores_list2[int(pdb_file_content2[5])-residue_pdb_start])
        pdb_file_content2 = str(pdb_file_content2).replace("[","")
        pdb_file_content2 = str(pdb_file_content2).replace("]","")
        pdb_file_content2 = str(pdb_file_content2).replace("'","")
        print str(pdb_file_content2) + "\n"
        all_results = all_results + str(pdb_file_content2)+"\n"
    
    

    #line_no = line_no + 1

#print str(all_results)


target_file = open("result.pdb", "w")
target_file.write(str(all_results))
pdb_file2.close()
target_file.close()


#Edit the PDB file line by line - END



