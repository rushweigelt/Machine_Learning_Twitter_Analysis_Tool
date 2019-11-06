'''
Rush Weigelt

Logistical Regression for TAT

11.4.19
'''
import csv
import os
#Data file names. Files must be csvs and located in the 'data' folder
filename = 'chinaBotsUnlabelled.csv'
#Change these to the applicable fieldnames to be counted
urls = 'urls'
hashtags = 'hashtags'
mentions = 'user_mentions'

#creating directory locations for applicable places in dir
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), "../../../"))
data_folder = os.path.join(parentDirectory, "data", "preprocessed", "count")
out_folder = os.path.join(parentDirectory, "data", "preprocessed", "standardizeFieldnames")
data_file = os.path.join(data_folder, filename)
out_path = os.path.join(out_folder, filename[:-4]+"_counted.csv")

def CountListedData(filename):
    headers = []
    #rip headers
    with open(data_file, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = csv_reader.__next__()
        #append our new fieldnames: num_hashtags, num_urls, label
        headers.append('num_hashtags')
        headers.append('num_urls')
        headers.append('num_mentions')
        csv_file.close()
    #Open a reader and writer, add columns for number of urls and hashtags
    with open(out_path, 'w', encoding='latin-1', newline='') as csv_file2:
        csv_writer = csv.DictWriter(csv_file2, fieldnames=headers)
        csv_writer.writeheader()
        with open(data_file, mode='r', encoding='latin-1') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                #count urls
                url_count = 0
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
                mention_count = 0
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
    print("Done Creating Temp Data")
    csv_file.close()
    csv_file2.close()


def main():
    CountListedData(filename)

if __name__ == "__main__":
    main()