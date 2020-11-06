#!/bin/bash
echo "--------------------------------------------------------------------------"
echo "Installing pip requirements" 
pip install -r requirements.txt
echo "--------------------------------------------------------------------------"
echo "Installing fairseq" 
sudo pip install --editable ../fairseq/
echo "--------------------------------------------------------------------------"
