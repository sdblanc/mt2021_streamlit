# Import the libraries
import nltk
import torch
from nltk.tokenize.treebank import TreebankWordDetokenizer
from fairseq.models.roberta import RobertaModel

# Streamlit specific libraries
from PIL import Image
import streamlit as st

class Experiment_1():
    def __init__(self):
        # # Create a title and a subtitle
        st.write("""
        # Experiment 1: Artificial Student
        For this experiment, an Artificial Student was created. It's job is to solve Dutch fill-in-the-gap questions.
        This AI is built upon RobBERT, a dutch based RobBERTA language model.
        """)

        # # Open and display an image in the webapp
        image = Image.open('./img/image-23-1.jpg')
        # # Display the image
        st.image(image, caption='Fig 1: RobBERT is the model of which this Artificial Student is based upon.', use_column_width = True)

        model = RobertaModel.from_pretrained(
            '../models/robbert/',
            checkpoint_file='RobBERT-base.pt',
        )
        model.eval()  # disable dropout

        st.subheader('Example of a fill-in-gap question')
        st.write("""Question = `Het meisje <mask> daar loopt.` \n 
        Number of results = 4""")
        text = 'Het meisje <mask> daar loopt.'
        no_results = 4
        st.write("Results: ")
        results = model.fill_mask(text, no_results)
        for i,r in enumerate(results):
            st.write("Result #",str(i),": ",r)

        st.subheader('Try it out for yourself!')
        text = st.text_area("Enter a sentence with a gap indicated with '<mask>' as shown in the example above.", "Type Here...")
        if st.button("Predict"):
            results = model.fill_mask(text, no_results)
            st.write(results)

