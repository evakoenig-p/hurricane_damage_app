import os
import gdown
import streamlit as st  
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np


def predict_image_class(image_data, model, w=128, h=128):
        size = (w,h)
        image = ImageOps.fit(image_data, size, Image.LANCZOS)
        img = np.asarray(image)
        if len(img.shape) > 2 and img.shape[2] == 4:
        #slice off the alpha channel if it exists
          img = img[:, :, :3]
        img = np.expand_dims(img, axis=0) # for models expecting a batch
        prediction = model.predict(img)
        return prediction


@st.cache_resource
def load_model():
    model=tf.keras.models.load_model('Hurricane_Classifier2.keras')
    return model


st.set_page_config(
    page_title="Hurricane Detector",
#    page_icon = ":cat:",
    initial_sidebar_state = 'auto'
)

with st.sidebar:
        #st.image('image_path.png')
        st.title("Hurricane Detector")
        st.subheader("Description of what your model is doing.")

st.write("""
         # Hurricane Detector
         """
         )

img_file = st.file_uploader("", type=["jpg", "png"])

if 'Hurricane_Classifier2.keras' not in os.listdir():
        with st.spinner('Model is being downloaded...'):
                gdown.download(id='1B-VSxxmTLYC7O-pMYPqby7a1MSE56dUA')
with st.spinner('Model is being loaded...'):
  model=load_model()

if img_file is None:
    st.text("Please upload an image file")
else:
  image = Image.open(img_file)
  st.image(image, use_container_width=False)
  predictions = predict_image_class(image, model)

  #### FOR THIS EXAMPLE ONLY
  #top5_preds = tf.keras.applications.imagenet_utils.decode_predictions(predictions, top=5)
  #st.info(top5_preds[0])
  #top_pred = top5_preds[0][0][1]
  #################
        
  prediction= np.argmax(predictions,axis=1)
  st.info('0: no Hurricane, 1:Hurricane')
  st.info(prediction)     
  #string = "Detected class: " + prediction

  answer = {0: 'no Hurricane',1:'Hurricane'}     

  if prediction[0] == 0 :        
      st.write("""
        # No Hurricane """)
  else:                
      st.write("""
        # Hurricane """)
 #  st.sidebar.warning(string)
 #   st.markdown("## Issue detected:")

#if 'cat' in top_pred.lower() or top_pred.lower() == 'tabby':
#    st.balloons()
##    st.sidebar.success(answer[prediction])
#    st.write("""
#    # Hurricane """)
#  else:
#    st.sidebar.warning(string)
#    st.markdown("## Issue detected:")
 #   st.info("No Hurricane")
