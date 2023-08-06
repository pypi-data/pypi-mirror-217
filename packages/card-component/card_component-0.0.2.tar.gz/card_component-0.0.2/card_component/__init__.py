import os
import streamlit.components.v1 as components


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("card_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "card_component",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("card_component", path=build_dir)


def card_component(title, img_path, body, pdf_cnts, key=None, on_click=None):
    """Create a new instance of "card_component".
    """

    component_value = _component_func(title=title,
                                      img_path=img_path,
                                      body=body,
                                      pdf_cnts=pdf_cnts,
                                      key=key, default=0)

    return component_value

if not _RELEASE:
    import pandas as pd

    import streamlit as st
    from streamlit_extras.switch_page_button import switch_page
    
    # 초기 변수는 세션에 몽땅 저장하지 않으면 머리 아파진다
    # ========================================================
    if 'etfs' not in st.session_state:
        st.session_state['etfs'] = pd.read_csv('/home/moongtnt/workplace/miraeasset/demo/component-template/template/card_component/db/theme_etfs.csv')
        
    if 'ticker' not in st.session_state:
        st.session_state['ticker'] = None
    # ========================================================
        
    st.set_page_config(layout='wide')
        
    etfs = st.session_state['etfs']
    
    st.title('미래에셋증권 다이렉트 인덱싱(Demo)')
    
    st.markdown('---')
    left_margin, col, right_margin = st.columns([1, 4, 1])
    
    with col:
        st.subheader('테마형 ETF로 시작해보세요')
    
    left_margin, col1, col2, col3, col4, right_margin = st.columns(6)
    
    with col1:
        for i in range(0, len(etfs), 4):
            if card_component(title=etfs['theme'][i],
                           img_path=f"/images/{etfs['img_file_name'][i]}",
                           body='20.15',
                           pdf_cnts=str(etfs['symbol'][i])):
                st.session_state['ticker'] = etfs['symbol'][i]
                switch_page('dashboard')
                
    with col2:
        for i in range(1, len(etfs), 4):
            if card_component(title=etfs['theme'][i],
                           img_path=f"/images/{etfs['img_file_name'][i]}",
                           body='20.15',
                           pdf_cnts=str(etfs['symbol'][i])):
                st.session_state['ticker'] = etfs['symbol'][i]
                switch_page('dashboard')
                
    with col3:
        for i in range(2, len(etfs), 4):
            if card_component(title=etfs['theme'][i],
                           img_path=f"/images/{etfs['img_file_name'][i]}",
                           body='20.15',
                           pdf_cnts=str(etfs['symbol'][i])):
                st.session_state['ticker'] = etfs['symbol'][i]
                switch_page('dashboard')
    with col4:
        for i in range(3, len(etfs), 4):
            if card_component(title=etfs['theme'][i],
                           img_path=f"/images/{etfs['img_file_name'][i]}",
                           body='20.15',
                           pdf_cnts=str(etfs['symbol'][i])):
                st.session_state['ticker'] = etfs['symbol'][i]
                switch_page('dashboard')


    

