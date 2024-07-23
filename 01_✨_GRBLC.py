##############################################################################
# Imports
##############################################################################

import streamlit as st

from grblc.lightcurve import Lightcurve
from grblc.photometry.constants import grbinfo
# from streamlit_navigation_bar import st_navbar


# Page config

apptitle = "GRBLC"

st.set_page_config(page_title=apptitle, layout='wide')

st.title("Gamma Ray Bursts Optical Afterglow Repository", anchor="main")

st.markdown("""
    We present the indivudual optical/IR photometry of each one of the 535 GRBs gathered in [Dainotti et al.(2024)](https://doi.org/10.1093/mnras/stae1484)
    as well the spectral information of each observation.
    """
)


# Initialise session state keys

if 'select_event' not in st.session_state:
    st.session_state['select_event'] = "970228A"

if 'data_type' not in st.session_state:
    st.session_state['data_type'] = 'converted'

# if 'appx' not in st.session_state:
#     st.session_state['appx_bands'] = False

# if 'outliers' not in st.session_state:
#     st.session_state['remove_outliers'] = False

# if 'best' not in st.session_state:
#     st.session_state['best'] = False

# if 'start' not in st.session_state:
#     st.session_state['start'] = False


# App contents

## Analysis options
st.sidebar.markdown("## Select GRB")
st.session_state['select_event'] = st.sidebar.selectbox("*Mandatory field", grbinfo.index)

## Information
st.sidebar.markdown("## Information")
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 25px;
}
</style>
""",
    unsafe_allow_html=True,
)


with st.container():
    st.sidebar.metric("## Right ascension", grbinfo.loc[grbinfo.index == st.session_state['select_event'], "ra"].to_numpy()[0])
    st.sidebar.metric("## Declination", grbinfo.loc[grbinfo.index == st.session_state['select_event'], "dec"].to_numpy()[0])
    st.sidebar.metric("## Redshift", grbinfo.loc[grbinfo.index == st.session_state['select_event'], "z"].to_numpy()[0])
    st.sidebar.metric("## Optical spectral index", str(grbinfo.loc[grbinfo.index == st.session_state['select_event'], "beta"].to_numpy()[0]) +
                       "+/-" + str(grbinfo.loc[grbinfo.index == st.session_state['select_event'], "beta_err"].to_numpy()[0]))


## Plot Lightcurve
plot = st.empty()

format = st.checkbox("Show raw data before homogenisation of photometric system and extinction correction")
if format:
    st.session_state['data_type']  = 'raw'

## Create Lightcurve object
lc = Lightcurve(
                grb = st.session_state['select_event'],
                path = st.session_state['data_type'],
                data_space = 'lin',
                save = False
                )
                
plot.plotly_chart(lc.displayGRB())


## Spectral analysis

c1, c2 = st.columns(2)

beta = c1.button(label=r"Calculate $\beta_{opt}$")
beta_opt = None
best = None
start = None

if beta:

    st.warning("This action may take a while. Click start to confirm.")# You can also get the best-fit parameter instead.")

#     c3, c4 = st.columns(2)
#     st.session_state['best'] = c3.button("Get best-fit")
#     st.session_state['start'] = c4.button("Start")


# if st.session_state['best']:
#     st.write(f"The best-fit value from our analysis in [Dainotti et al.(2024)](https://doi.org/10.1093/mnras/stae1484) is {beta_opt}")

#     st.session_state['best'] = False

# if st.session_state['start']:
    st.markdown("## Spectral Analysis")
    st.write("Fitting SMC, LMC and MW model based on Pei (1992). The best model is selected based on probability. Please see [Dainotti et al.(2024)](https://doi.org/10.1093/mnras/stae1484) for additional details.")

    with st.spinner("This may take a while. Please do not exit the page."):
        dfexp = lc.betaGRB()

    st.write("### Our calculation:")
    if len(dfexp) == 0:
        st.error(r"No viable $\beta_{opt}$ calculated. Refer Dainotti et al. 2024 for more details.")
    else:
        st.table(dfexp)

    # st.session_state['start'] = False


## Download

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep='\t').encode('utf-8')

txt = convert_df(lc.df)

c2.download_button(
        label="Download data",
        data=txt,
        file_name=st.session_state['select_event']+st.session_state['data_type']+'.txt',
        mime='text/csv',
    )
    
