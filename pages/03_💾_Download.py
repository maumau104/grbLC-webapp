# Author: Vysakh P A, Updated by: Ridha Fathima Mohideen Malik

import streamlit as st

import os
import shutil
from zipfile import ZipFile

import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

from grblc.photometry.constants import grbinfo
from grblc.data.load import get_grb


# Download page
st.markdown("# Download")

# Logo

custom_css = """
<style>
img[data-testid="stLogo"] {
    height: 15rem;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.logo('logo.png', icon_image='logo.png')

## Cleaning download directory on each new session
if 'file_zip' not in st.session_state: 
    if os.path.exists('download_folder/') == True:
        shutil.rmtree('download_folder/')

catalog = grbinfo.copy() # to avoid cache issues affecting other pages


## Some essential fucntions
def relation_checker(
    ra_max, 
    ra_min, 
    dec_max, 
    dec_min, 
    z_max, 
    z_min
):
    """
    Function to ensure max > min for all slider variables.

    """

    if (ra_max > ra_min) & (dec_max > dec_min) & (z_max > z_min):
        return 1
    else:
        return 0


def download_option(
    catalog, 
    ra_max, 
    ra_min, 
    dec_max, 
    dec_min, 
    z_max, 
    z_min,
    converted
):
    """
    Function to generate zip file to download.

    """
 
    if (np.sum(np.array([ra_max, ra_min, dec_max, dec_min, z_max, z_min]) == '-') > 0) \
        and not (relation_checker(ra_max, ra_min, dec_max, dec_min, z_max, z_min)):
        st.write("Enter proper values!")

    else:
        download_range = catalog.loc[(catalog.ra >= ra_min) & (catalog.ra <= ra_max) & \
                                    (catalog.dec >= dec_min) & (catalog.dec <= dec_max) & \
                                    (catalog.z >= z_min) & (catalog.z <= z_max)
                                    ]
        
        file_zip = 'download_folder/'+str(np.round(ra_min,decimals=1)) + str(np.round(ra_max,decimals=1)) + '_'  +\
                        str(np.round(dec_min,decimals=1)) + str(np.round(dec_max,decimals=1)) + '_' + \
                            str(np.round(z_min,decimals=1)) + str(np.round(z_max,decimals=1)) + '.zip'
        
        try:
            os.mkdir('download_folder')
        except FileExistsError:
            pass

        type = 'raw'
        if converted:
            type = 'converted'
        
        files_found = len(download_range)
        with ZipFile(file_zip, 'w') as zipObj2:
            for grb in download_range.index:
                try:
                    zipObj2.write(get_grb(grb, type))
                except FileNotFoundError:
                    st.warning(grb+" not found.")
                    files_found -= 1

        return file_zip, files_found


## Connecting to streamlit

c = SkyCoord(catalog.ra.to_numpy(),
            catalog.dec.to_numpy(),
            frame='icrs'
            )

catalog['ra'] = c.ra.deg
catalog['dec'] = c.dec.deg

min_z = min(catalog.z.to_numpy())
max_z = max(catalog.z.to_numpy())

if 'filename' not in st.session_state:
    st.session_state.file_zip = None

with st.form("download_form"):

    ra_min, ra_max = st.slider(
            'Right Ascension',
            0.0, 360.0, step=0.0001, value =(0.0, 360.0))

    dec_min, dec_max = st.slider(
            'Declination',
            -90.0, 90.0, step=0.0001, value =(-90.0, 90.0))
    z_min, z_max = st.slider(
            'Redshift',
            min_z, max_z, step=0.0001, value =(float(min_z), float(max_z)))
    
    converted = st.checkbox("AB converted and extinction corrected files")
    
    submitted = st.form_submit_button("Generate Download Link")

    if submitted:
        st.session_state.file_zip, files_found = download_option(catalog, ra_max, ra_min, dec_max, dec_min, z_max, z_min, converted)        


if st.session_state.file_zip != None:

    with open(st.session_state.file_zip, 'rb') as f:

        st.write(str(files_found) + ' GRB files found. Click the button below to download the zip file.')

        st.download_button('Download Zip', f, file_name=st.session_state.file_zip)
