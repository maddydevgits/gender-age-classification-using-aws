import boto3
import streamlit as st
from PIL import Image
import os

accessKey='' # ask admin to share access key
secretAccessKey='' # ask admin to share secret access
region='us-east-1'

st.title('Gender and Age Classification using AWS')

def load_image(img):
    return Image.open(img)

src_file=st.file_uploader('Upload Image',type=['png','jpg','jpeg'])

if src_file is not None:
    file_details={}
    file_details['name']=src_file.name
    file_details['type']=src_file.type
    file_details['size']=src_file.size
    st.write(file_details)

    st.image(load_image(src_file),width=250)

    with open(os.path.join('uploads','src.jpg'),'wb') as f:
        f.write(src_file.getbuffer())
    
    image=open('uploads/src.jpg','rb')
    client=boto3.client('rekognition',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    response=client.detect_faces(Image={'Bytes':image.read()},Attributes=['ALL'])
    # st.write(response)
    age=response['FaceDetails'][0]['AgeRange']
    gender=response['FaceDetails'][0]['Gender']['Value']
    st.success('Age Range: ' + str(age['Low']) + '-' + str(age['High']))
    st.success('Gender: '+ gender)


