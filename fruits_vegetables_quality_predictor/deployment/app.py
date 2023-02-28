import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

st.set_page_config(
    page_title="Fruit and Vegetable Quality Predictor",
    page_icon='🍎',
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/mfadlili',
        'Report a bug': "https://github.com/mfadlili",
        'About': "# This is hacktiv8 FTDS milestone 2 Phase 2."
    }
)

st.title('Fruit and Vegetable Quality Predictor')
st.image('mfadlili/DS_Project/blob/main/fruits_vegetables_quality_predictor/deployment/fruits_vegetables.jpg')
st.write('Only photos of apples, bananas, bitter gourd, capsicum, oranges, and tomatoes can be used to create predictions using this application. ')
dict_class = {0: 'Fresh Apple',
 1: 'Fresh Banana',
 2: 'Fresh Bitter Gourd',
 3: 'Fresh Capsicum',
 4: 'Fresh Orange',
 5: 'Fresh Tomato',
 6: 'Stale Apple',
 7: 'Stale Banana',
 8: 'Stale Bitter Gourd',
 9: 'Stale Capsicum',
 10: 'Stale Orange',
 11: 'Stale Tomato'}

select = st.selectbox('Please select image source:', ('Upload image', 'Take a photo'))
model = load_model("https://github.com/mfadlili/DS_Project/blob/main/fruits_vegetables_quality_predictor/deployment/fruit_veg_model.h5?raw=true")
if select=='Upload image':
    file = st.file_uploader("", type=["jpg","png"])
    col1, col2 = st.columns(2)

    with col2:
        if st.button('Show the image'):
            if file is not None:
                st.image(file)

    with col1:
        if st.button('Predict'):
            img = image.load_img(file, target_size=(128,128))
            x = image.img_to_array(img)
            classes = np.argmax(model.predict(np.array([x])/255))
            st.title(dict_class[classes])
else:
    picture = st.camera_input('Ambil foto anda.')
    if st.button('Predict '):
        img = image.load_img(picture, target_size=(128,128))
        x = image.img_to_array(img)
        classes = np.argmax(model.predict(np.array([x])/255))
        st.title(dict_class[classes])
