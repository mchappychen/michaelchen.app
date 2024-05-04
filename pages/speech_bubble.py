
import streamlit as st
from PIL import Image
from PIL import ImageOps
import io

def resize_and_overlay(speech_bubble, background, flip=False):
    speech_bubble_img = Image.open(speech_bubble)
    background_img = Image.open(background)
    background_img = ImageOps.exif_transpose(background_img)
    new_width = background_img.width
    ratio = new_width / speech_bubble_img.width
    new_height = int(speech_bubble_img.height * ratio)
    resized_speech_bubble = speech_bubble_img.resize((new_width, new_height), Image.LANCZOS)

    if flip:
        resized_speech_bubble = resized_speech_bubble.transpose(Image.FLIP_LEFT_RIGHT)

    background_img.paste(resized_speech_bubble, (0, 0), resized_speech_bubble)

    return background_img

st.title("This is you talkin")

background_file = st.file_uploader("Upload Background Image", type=["jpg", "jpeg", "png"])
flip = st.checkbox("Flip Speech Bubble Left to Right")

if background_file:
    # Perform overlay and display resulting image
    overlayed_img = resize_and_overlay('disc.jpeg', background_file, flip)
    st.image(overlayed_img, caption="Overlayed Image", use_column_width=True)

    img_bytes = io.BytesIO()
    overlayed_img.save(img_bytes, format='PNG')
    st.download_button(label="Download Overlayed Image", data=img_bytes.getvalue(), file_name="overlayed_image.png", mime="image/png")


