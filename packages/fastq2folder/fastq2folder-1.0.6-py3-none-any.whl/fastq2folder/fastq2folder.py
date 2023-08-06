#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import gzip
import shutil
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from Bio import SeqIO
from scipy import stats
import numpy as np

#Create a new folder for the unzipped and binned files to go
#base_dir = r"C:\Users\egar1\OneDrive\Desktop"
base_dir = input('Enter path to source directory: ')
if os.path.isdir(base_dir):
    print('The directory exists')
else:
    print('The directory does not exist.  Make sure you select the parent directory, and omit outer quotes and the final forward slash.')
file_dir = 'fastq_pass'
source_dir = os.path.join(base_dir, file_dir)
new_dir = 'fastq_bins'

if os.path.isdir(source_dir):
    print('Found the fastq_pass folder')
else:
    print('The fastq_pass folder does not exist in the source directory.') 

destination_dir = os.path.join(base_dir, new_dir)
if not os.path.isdir(destination_dir):
    os.mkdir(destination_dir)
    print('folder created')
    
for foldername, subfolders, filenames in os.walk(source_dir):
    #print('foldername', foldername)
    #print('subfolders', subfolders)
    #print('filenames', filenames)
    for filename in filenames:
        shutil.copy(os.path.join(foldername, filename), destination_dir)

# Create a dictionary to store the barcode folders
barcode_folders = {}

def decompress_gz_files_in_dir(directory):
    for item in os.listdir(directory):
        if item.endswith('.gz'):
            print('decompressing ', item)
            file_name = os.path.join(directory, item)
            with gzip.open(file_name, 'rb') as f_in:
                with open(file_name[:-3], 'wb') as f_out:  # Remove the '.gz' from the output file name
                    shutil.copyfileobj(f_in, f_out)
    print('decompression complete')

# Call the function and provide the directory you want to decompress .gz files in
decompress_gz_files_in_dir(destination_dir)


# In[2]:


import glob
import re

output_directory = os.path.join(destination_dir, 'pooledFiles')
print('output dir', output_directory)

# Ensure that the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Get a list of all fastq files
files = glob.glob(os.path.join(destination_dir, '*.fastq'))
print('files', files)

# Regular expression to match barcodes
barcode_pattern = re.compile(r'barcode\d+')

# Group files by barcode
barcode_to_files = {}
for file in files:
    # Extract barcode from file name using the regular expression
    barcode = barcode_pattern.search(os.path.basename(file))
    print(barcode)
    if barcode is not None:
        barcode = barcode.group()
        if barcode not in barcode_to_files:
            barcode_to_files[barcode] = []
        barcode_to_files[barcode].append(file)

# Combine files with the same barcode
for barcode, files in barcode_to_files.items():
    with open(os.path.join(output_directory, f'{barcode}_combined.fastq'), 'w') as outfile:
        for file in files:
            with open(file) as infile:
                for line in infile:
                    outfile.write(line)


# In[3]:


##VERSION2
from collections import Counter
import numpy as np
import scipy.stats as stats

print('calculating read lengths')
#TODO: consolidate fastq files from the same barcode
def get_stats(fastq_file):
    cutoff_value = 1000
    lengths = []
    filtered = []
    for record in SeqIO.parse(fastq_file, "fastq"):
        lengths.append(len(record.seq))
    for n in lengths:
        if n > cutoff_value:
            filtered.append(n)
    if len(filtered) > 0:
        counter = Counter(filtered)
        max_count = max(counter.values())
        modes = [item for item, count in counter.items() if count == max_count]
        if max_count == 1:
            print('All read lengths occur only once')
            mode_or_avg = round(np.average(lengths))
        elif len(modes) > 1:
            print('Multiple modes detected')
            mode_or_avg = round(np.average(modes))
        else:
            print('Single mode detected')
            mode_or_avg = modes[0]
        return lengths, filtered, mode_or_avg
    else:
        print('Not enough long reads for statistical analysis')
        return None, None, None
    
results = []

# define the bins and their labels
bins = [0, 3000, 6000, 9000, 12000, 15000, 18000, np.inf]
labels = ['bin2000', 'bin5000', 'bin8000', 'bin11000', 'bin14000', 'bin17000', 'bin20000']

#INPUT is a folder of fastq files
for file in os.listdir(output_directory):
    if not file.endswith(".fastq"):
        continue
    print('calculating statistics: ', file)
    fastq_file = os.path.join(output_directory, file)
    
    lengths, filtered, mode_or_avg = get_stats(fastq_file) #unpack return values from get_stats
    
    if mode_or_avg is not None:
        bin_labels = pd.cut(filtered, bins=bins, labels=labels)

        # Identify the most frequent bin for this file
        common_bin = pd.DataFrame(bin_labels).mode().values[0][0]

        results.append({
            "Barcode": file,
            "Estimated read length": mode_or_avg,
            "Bin": common_bin
        })

        new_dir = os.path.join(destination_dir, common_bin)
        os.makedirs(new_dir, exist_ok=True)

        shutil.copy2(fastq_file, os.path.join(new_dir, file))

df = pd.DataFrame(results)
print(df)
print('Binning complete')


# In[4]:


import matplotlib.backends.backend_pdf
import matplotlib.gridspec as gridspec
import seaborn as sns

from matplotlib import pyplot as plt

def plot_histograms(directory):
    # Create a new PDF file
    sns.set(font_scale=1.75)
    sns.set_style("white")
    #sns.color_palette("viridis", as_cmap=True)
    
    
    output_file = destination_dir+"\\read_length_histograms.pdf"
    print(output_file)
    pdf = matplotlib.backends.backend_pdf.PdfPages(output_file)

    file_list = [file for file in os.listdir(directory) if file.endswith(".fastq")]
    num_pages = len(file_list) // 8 + (len(file_list) % 8 > 0)

    for page in range(num_pages):
        print('drawing histograms page', page+1)
        # Create a new figure for each page
        fig = plt.figure(figsize=(20, 28))
        
        if page == 0:
            fig.suptitle('Genetic Design and Engineering Center\nWhole Plasmid Sequencing', font = 'Arial', fontsize=20, y=.925)
        plt.subplots_adjust(top=0.85, bottom=0.15)


        gs = gridspec.GridSpec(4, 2)
        
        # Adjust vertical spacing
        gs.update(hspace=0.5) # Change the value as needed for more or less spacing

        for i in range(min(8, len(file_list) - page * 8)):
            file = file_list[page * 8 + i]
            fastq_file = os.path.join(directory, file)
            
            #estimate the length in bp
            lengths, filtered, mode_or_avg = get_stats(fastq_file) #unpack return values from get_stats
            
            ax = fig.add_subplot(gs[i // 2, i % 2])

            if lengths is not None:
                # Plot histogram
                color = sns.husl_palette(8)
                sns.histplot(lengths, bins=100, kde=False, ax=ax, zorder=1, color =color[6])

                # Add a vertical line for the mode
                if mode_or_avg is not None:
                    print('mode ', mode_or_avg)
                    ax.axvline(mode_or_avg, color='black', linestyle='dashed', linewidth=2, alpha=0.5)

                    # Annotate the mode
                    ax.text(0.97, 0.94, f'Estimated plasmid size: {mode_or_avg}bp', fontsize=14, font = 'Arial',horizontalalignment='right', 
                            verticalalignment='top', transform=ax.transAxes, color='black', zorder=2)

                    # Annotate the number of reads
                    ax.text(0.97, 0.87, f'Reads: {len(lengths)}', fontsize=14, font = 'Arial', horizontalalignment='right', 
                            verticalalignment='top', transform=ax.transAxes, color='black', zorder=2)
                    
                    if len(lengths) < 50:
                        ax.add_patch(plt.Rectangle((0,0), 1, 1, fill=True, color='white', alpha=0.7, transform=ax.transAxes, zorder=3))
                        ax.text(0.5, 0.5, 'Insufficient Reads', fontsize=20, font = 'Arial', color='black', ha='center', va='center', transform=ax.transAxes, zorder=4)                        
                
            else:
                ax.add_patch(plt.Rectangle((0,0), 1, 1, fill=True, color='white', alpha=0.5, transform=ax.transAxes, zorder=3))
                ax.text(0.5, 0.5, 'Insufficient Reads', fontsize=20, font = 'Arial', color='black', ha='center', va='center', transform=ax.transAxes, zorder=4)
            
            # Get the barcode from the file name
            barcode = file.split('pass_')[-1]
            barcode = barcode[:9]
            print(barcode)

            # Set the title to the barcode
            ax.set_title(barcode, fontsize=40, font = 'Arial')
            
            # Label the axes
            ax.set_xlabel('Sequence Length', font = 'Arial', fontsize=14)
            ax.set_ylabel('Count', font = 'Arial', fontsize=14)
        
        # Add the figure to the PDF file
        pdf.savefig(fig)

    # Close the PDF file
    pdf.close()
plot_histograms(output_directory)

