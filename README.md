# mt2021_streamlit
This repository wil contain the streamlit code for the RobBERT experiments of Silas Deblanc.

# Installation
Step 1: Clone the fairseq repository for installation (https://github.com/pytorch/fairseq)<br>
<code> git clone https://github.com/pytorch/fairseq </code>

Step 2: Install requirements using scripts
<code> ./install_script.sh</code>

Step 3: Run the app
<code> streamlit run WebApp.py</code>

Extra: You can download the RobBERT model from https://github.com/iPieter/BERDT/releases/download/v1.0/RobBERT-base.pt. This model uses the default RobBERTa dictionary which you can download using <code> wget -N 'https://dl.fbaipublicfiles.com/fairseq/gpt2_bpe/dict.txt' </code>

<!-- Note for myself: Run 'conda activate mt_streamlit'  -->