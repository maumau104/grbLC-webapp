import streamlit as st

from grblc.lightcurve import Lightcurve
from grblc.photometry.constants import grbinfo


st.markdown("### Colour Evolution")


# Initialise session state keys

if 'select_event' not in st.session_state:
    st.session_state['select_event'] = "970228A"

if 'data_type' not in st.session_state:
    st.session_state['data_type'] = 'converted'

if 'outliers' not in st.session_state:
    st.session_state['remove_outliers'] = False

if 'select_band' not in st.session_state:
    st.session_state['select_band'] = 'mostnumerous'


## Set data

st.session_state['select_event'] = st.sidebar.selectbox("*Mandatory field", grbinfo.index)

pos1 = st.sidebar.empty()

outliers = st.sidebar.checkbox(label="Remove outliers")

if outliers:
    st.session_state['remove_outliers'] = True

## Create Lightcurve object
lc = Lightcurve(
                grb = st.session_state['select_event'],
                path = st.session_state['data_type'],
                data_space = 'lin',
                appx_bands = True,
                remove_outliers = st.session_state['remove_outliers'],
                save= False
                )

filters = [*set(lc.band)] # TO DO: order by band count. display band count
st.session_state['select_band'] = pos1.selectbox("Choose the band, by default the most numerous", filters)

st.markdown("")
colorevolplot = st.empty()

st.markdown("")
colorevoltab = st.empty()

fig_avar, fig_a0, filterforrescaling, \
    nocolorevolutionlist, colorevolutionlist, nocolorevolutionlista0, colorevolutionlista0, \
        light, resc_slopes_df, rescale_df = lc.colorevolGRB(save=False)

colorevolplot.pyplot(fig_avar)

colorevoltab.table(resc_slopes_df)

st.markdown("## Rescaling")

rescaleplot = st.empty()

try:
    figunresc, figresc, resc_mag_df = lc.rescaleGRB(save=False)

    rescaleplot.pyplot(figresc)

except ValueError:
    st.error("No filters to rescale.")