import streamlit as st

from src.utils import FIGURE_8, FIGURE_9, FIGURE_10

st.set_page_config(
    page_title="Danger Zones",
    page_icon="🚑",
    layout="wide"
)
st.write("# Danger Zones in France 🚑")
st.write("#")
st.markdown("""
The goal of the project asked for the creation of Danger Zones indicating regions
of France which are more risky in terms of traffic flow and its fatalities.
The Risk Score was born out of the idea to score each zone according to its risks
based on the number of accidents, the type of accidents and other factors
contributing to its score where 1 is lower risk and 4 being the highest risk. The Risk
Score can be simply calculated as the weighted average of factors influencing the
likelihood of having a fatality or injury given certain data variables

```
Risk Score = α×[Primary Factors] + β×[Secondary Factors]
```

where the weights can be set with α being a stronger weight , see code for
understanding the score. The score then can be used as a visualization tool to see
which zones of France are more riskier or dangerous in terms of traffic flow(see Figure 10)
One thing we notice that Paris has a lower risk score even though it has a large number of accidents. The two main reasons is the ```H3_RESOLUTION``` and an abundance of ```MINOR INJURY```
. This shifts the weight down to a lower value however we can also see the number of values for the risk score for Paris overshadows the rest of France which fits our hypothesis that Paris is quite dangerous in terms of traffic accidents.

""")
st.write("#")
st.image(FIGURE_10, caption="Figure 10: Danger Zone Plot of France using the RiskScore")

