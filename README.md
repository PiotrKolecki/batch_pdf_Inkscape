# Description
Batch export pdf with changing varaible text from Inkscape.

# Example of use
* invitations with variable names
* user guide with room phone number

# Requirements
* inkscape in $PATH
* python packages:
  * inkex
  * pathlib
  * lxml
    * etree
  * subprocess
  * os

# How to use
* Create an inkscape file (.svg)
* Create text file with 
* Modify script
  * change svg file name (svg_input)
  * change txt file name (file1)
  * change variable name (text_to_replace)
* run script with **python topdf.py**

Make sure the **text_to_replace** is exactly the same as in Inkscape

# How it works?
* It looks for nodes to change in svg that contain text_to_replace
* For each row in text file, changes the text and saves to file
* Then it runs a silent inkscape process to export to pdf
