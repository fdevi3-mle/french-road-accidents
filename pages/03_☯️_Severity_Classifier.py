import logging
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly_resampler import register_plotly_resampler




st.set_page_config(
    page_title="Severity Classifier",
    page_icon="☯️",
    layout="wide"
)
st.write("# Severity Classifier ☯️")

st.markdown("""
The severity classifier describes a model capable of predicting the severity of the
road accident when provided with data relating to GPS coordinates and other variables.


We first decided to classify the target as either being a Major injury or a Minor
injury, which would address a bit of the imbalance. Even with this imbalance we
decided to use a sampling method (SMOTE)[^1]

```
{MAJOR_INJURY: 1, MINOR_INJURY: 0}
```


[^1]: https://imbalanced-learn.org/stable/references/generated/imblearn.over_sa
mpling.SMOTE.html
""")
