
from io import BytesIO
import math
from pathlib import Path
import tempfile
from typing import Sequence
from PIL import Image as pimg
import streamlit as st

def _read_files(files: Sequence[BytesIO]) -> Sequence[pimg.Image]:
    # read images from paths
    return [pimg.open(file) for file in files]

def _combine_images(images: Sequence[pimg.Image]) -> pimg.Image:
    per_sprite_h = max((image.height for image in images))
    per_sprite_v = max((image.width for image in images))

    row_cnt = int(math.sqrt(len(images)))
    col_cnt = math.ceil(len(images) / row_cnt)
    new_img = pimg.new("RGBA", (per_sprite_v * col_cnt, per_sprite_h * row_cnt))

    # split the images to new img
    for i, image in enumerate(images):
        row = i // col_cnt
        col = i % col_cnt
        new_img.paste(image, (col * per_sprite_v, row * per_sprite_h))

    return new_img
    

def _main():
    st.title("EasySpritePacker")
    uploaded_files = st.file_uploader("Upload files", type="png", accept_multiple_files=True)
    if uploaded_files and st.button("Combine"):
        imgs = _read_files(uploaded_files)
        new_img = _combine_images(imgs)
        with tempfile.TemporaryDirectory() as tempdir:
            out_file_path  = Path(tempdir).joinpath('res.png')
            new_img.save(out_file_path)
            with open(out_file_path, 'rb') as file:
                st.download_button("Get Result", data=file, file_name='output.png')

    

if __name__ == "__main__":
    _main()