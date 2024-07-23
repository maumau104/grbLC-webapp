import streamlit as st

![LOGO](logo.png)
st.markdown("# About")

## Information
##############################################################################

st.markdown("""
    We present the largest optical photometry compilation of Gamma-Ray Bursts (GRBs) with measured redshifts ($z$) ([Dainotti et al.(2024)](https://doi.org/10.1093/mnras/stae1484)). 
    Our dataset includes 64813 observations of 535 events (including upper limits) from 28 February 1997 to 18 August 2023. 
    Moreover, we introduce **GRBLC**, a user-friendly web tool for visualising the photometry data, coordinates, redshift, host-galaxy extinction, 
    and spectral indices for each event in our database. 
    
    Additionally, we have integrated a Gamma-ray Coordinate Network (GCN) scraper 
    within **GRBLC** to automate the collection of magnitudes from GCN circulars. The web tool also includes a **Python** package 
    for uniformly investigating colour evolution in GRBs. We compute the optical spectral indices of 138 GRBs, 
    and craft a novel procedure to infer the presence of colour evolution in GRBs. By providing a standardised format 
    and a centralised repository for optical photometry, our web-based archive represents a significant milestone towards 
    unifying various community efforts to collect GRB photometric data. 
    
    This comprehensive catalogue facilitates 
    population studies by offering light curves (LCs) with improved coverage, as it aggregates data from multiple ground-based observatories 
    and the Swift satellite. Consequently, these LCs can be employed to train future LC reconstructions, enhancing redshift inference capabilities. 
    Our data collection efforts also help fill orbital gaps in the Swift observations, particularly at critical points in the LCs, 
    such as the end of the plateau emission or the identification of jet breaks.
    """
)



## App Guide
##############################################################################

#st.write("### App demo")

#st.video('demo.webm', format="video/webm")
#st.video('https://youtu.be/5bFyADbBAAk', format='url')


## Usage policy
##############################################################################

st.markdown("""
    ### Usage Policy
    The data gathered in this catalogue was obtained by public sources and private communications. 
    The **GRBLC^^ package and web-based repository are designed to be open-access and available to all members of the community.
    All are welcome to use our software, though we ask that if the provided data or software is used in any publication,
    the authors cite this paper as well as include the following statement in the acknowledgments: 
        
    "Data used in our work is taken from the catalogue ([Dainotti et al.(2024)](https://doi.org/10.1093/mnras/stae1484)), and the original data sources are cited within."            
    """
)


## Links
##############################################################################

st.markdown("""
    ### Data availability  
    The data is available along with the Python package at the GitHub link below.
    """
)


'''
    [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/SLAC-Gamma-Rays/grbLC) 
    [![Paper](https://badgen.net/static/Paper/MNRAS/orange)](https://doi.org/10.1093/mnras/stae1484)

'''
st.markdown("<br>",unsafe_allow_html=True)

