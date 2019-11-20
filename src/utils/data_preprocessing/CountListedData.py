'''
Rush Weigelt
11.4.19

Preprocessing step #1

This script exists to quickly COUNT and ENUMERATE URLs, Mentions, and Likes if the data lists them as a string.
It is written to work in two ways:
1) Hand-change the applicable variables     RUN: python3 CountListedData.py
2) Enter filename when running.             RUN: python3 CountListedData.py filename(no .csv)

NOTES: File must be a csv
datafile must be located at data > preprocess > count
output located at data > preprocess > standardizeFieldnames
'''
import csv
import os
import sys

#Data file names. Files must be csvs and located in the 'data' folder
#CHANGE IF RUNNING SCRIPT ALONE
filename = 'chinaBotsUnlabelled.csv'
#Fieldnames for what we'll be enumerating
#MUST CHANGE TO RUN WITH SPECIFIC CSV FILES
urls = 'urls'
hashtags = 'hashtags'
mentions = 'user_mentions'


#creating directory locations for applicable places in dir
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), "../../../"))
data_folder = os.path.join(parentDirectory, "data", "preprocessed", "count")
out_folder = os.path.join(parentDirectory, "data", "preprocessed", "standardizeFieldnames")
data_file = os.path.join(data_folder, filename)
out_path = os.path.join(out_folder, filename[:-4]+"_counted.csv")

#Function, filename with file being in data > preprocess > count
def CountListedData(file_name):
    data_file = os.path.join(data_folder, file_name)
    headers = []
    #rip headers
    #Look at datafile, take headers, add our enumeration headers, then close file
    with open(data_file, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = csv_reader.__next__()
        #append our new fieldnames: num_hashtags, num_urls, label
        headers.append('num_hashtags')
        headers.append('num_urls')
        headers.append('num_mentions')
        csv_file.close()
    #Open a reader and writer, add columns for our enumeration columns we just created
    with open(out_path, 'w', encoding='latin-1', newline='') as csv_file2:
        csv_writer = csv.DictWriter(csv_file2, fieldnames=headers)
        csv_writer.writeheader()
        with open(data_file, mode='r', encoding='latin-1') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                #TODO: Make these toogable bools, rather than an assumed thing

                #count urls
                if row[urls] == '':
                    num_url = 0
                elif row[urls] == '[]':
                    num_url = 0
                else:
                    comma_count = row[urls].count(',')
                    if comma_count == 0:
                        num_url = 1
                    else:
                        num_url = comma_count+1
                #count hashtags
                if row[hashtags] == '':
                    num_hts = 0
                elif row[hashtags] == '[]':
                    num_hts = 0
                else:
                    comma_count_hts = row[hashtags].count(',')
                    if comma_count_hts == 0:
                        num_hts = 1
                    else:
                        num_hts = comma_count_hts+1
                # count mentions
                if row[mentions] == '':
                    num_mentions = 0
                elif row[mentions] == '[]':
                    num_mentions = 0
                else:
                    comma_count = row[urls].count(',')
                    if comma_count == 0:
                        num_mentions = 1
                    else:
                        num_mentions = comma_count + 1
                #append new columns to csv
                row['num_urls'] = num_url
                row['num_hashtags'] = num_hts
                row['num_mentions'] = num_mentions
                csv_writer.writerow(row)
    print("Done Creating New Counted Datafile.\nNew file is in data > preprocessed > standardizeFieldnames")
    csv_file.close()
    csv_file2.close()

#if we get an argument, it will be the filename. File must be in
#data > preprocess > count
def main():
    if len(sys.argv) <= 2:
        CountListedData(filename)
    else:
        CountListedData(sys.argv[1])

if __name__ == "__main__":
    main()