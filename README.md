# CSV-Maker

This repository contains a python script which takes in a folder or zipfile containing SEM images,
automatically extracts the embedded metadata from all of the tiff images, and summarizes each image's metadata
in a neatly formatted metadata table.

The inputs to the script are:

* a csv file which is used to convert between metadata headers and Hyperspy extracted dictionary keys. This file may be [accessed here](https://docs.google.com/spreadsheets/d/1f_9qKa2BbA5_q47ild_fZeQFKPUJKcxcbkYkhje0EF0/edit?usp=sharing).
* a directory or zip file containing the SEM tiff images which one would want to summarize
* the location of your save file

### Limitations

The script currently only works for SEM tiff files. Extensions for LM are ongoing.
