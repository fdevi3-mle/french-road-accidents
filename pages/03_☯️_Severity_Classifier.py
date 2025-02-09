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
road accident when provided with data relating to GPS coordinates and other variables.We first decided to classify the target as either being a Major injury or a Minor
injury, which would address a bit of the imbalance. Even with this imbalance we decided to use a sampling method (SMOTE)[^1]
```
{MAJOR_INJURY: 1, MINOR_INJURY: 0}
```
A Literature research showed that (Behboudi)[^2] showed us that simple machine learning models performed relatively well . So I tried out both a
Random Forest Classifier(RF) and a Gradient Boosting Classifier(GBC)

[^1]: https://imbalanced-learn.org/stable/references/generated/imblearn.over_sa
mpling.SMOTE.html
[^2]: Recent Advances in Traffic Accident Analysis and Prediction: A Comprehensive Review of Machine Learning Techniques.
""")

left_col,right_col = st.columns(2,border=True)

with left_col:
    st.subheader("Gradient Boosting Classifier")
    st.markdown("""
    Upon perusing through an interesting blog about GBC[^1] , it made sense to try out the GBC as it fit the example. Plus the GBC points towars a negative gradient/ weak hypothesis and
since our data being  imbalanced it can handle it well. Simply put its a bunch of learning from mistakes of many iterations of Decision Trees
We can quickly set up our GBC with the code as below.

```
def gradboost_classifier(X_train,X_test,y_train,y_test):
    params = {
        'n_estimators': [10,50,100,200,250,300,500],
        'max_depth': [1,2,5,7,10, None]}
    random_search = RandomizedSearchCV(GradientBoostingClassifier(random_state=random_state),cv=3,n_jobs=-1,param_distributions=params)
    random_search.fit(X_train,y_train)
    #joblib.dump(random_search.best_estimator_, ExtensionMethods.generate_filename("GradientBoostingClassifier",'pkl')) ## too heavy
    return random_search.best_estimator_
```
---
Ideally a brute force method(GridSearch) could provide a better model but we will
proceed with the RandomSearchCV which provided decent enough results for a
prototype project but would not pass my standard to deploy into production. The table below shows the classification report for the GBC Classifier

 ****             | **Precision**      | **Recall**         | **F1-Score**       
------------------|--------------------|--------------------|--------------------
 **MINOR**            | 0.8309882977261436 | 0.8262194801509307 | 0.8285970275113314 
 **MAJOR**            | 0.8276595301131981 | 0.8323968466957397 | 0.8300214289447552 
 **Accuracy**     | 0.8293121998582937 | 0.8293121998582937 | 0.8293121998582937 
 **Macro Avg**    | 0.8293239139196709 | 0.8293081634233352 | 0.8293092282280432 
 **Weighted Avg** | 0.8293217388255002 | 0.8293121998582937 | 0.8293101589650651 

The table shows GradientBoostClassifier(GBC) performed quite well
with an acceptable over 80 percent score values for both values.

[^1]: https://www.digitalocean.com/community/tutorials/gradient-boosting-for-classification
    """)


with right_col:
    st.subheader("Random Forest Classifier")
    st.markdown("""
    Random Forest Classifier(RF) is the best first choice model for a simple classification task and we modeled the RF as below
```
def rando_classifier(X_train,X_test,y_train,y_test):
    params = {
        'n_estimators': [10,50,100,200,250,300],
        'max_depth': [1,2,5,7,10,None]
     }
    random_search = RandomizedSearchCV(RandomForestClassifier(random_state=random_state),cv=3,n_jobs=-1,param_distributions=params)
    random_search.fit(X_train,y_train)
    return random_search.best_estimator_
```
---
 ****             | **Precision**      | **Recall**         | **F1-score**       |   
------------------|--------------------|--------------------|--------------------|
 **MINOR**            | 0.7643352782619051 | 0.7421145013295776 | 0.7530610068259385 |           
 **MAJOR**            | 0.7500356567982233 | 0.7717837973834284 | 0.7607543270472746 |          
 **Accuracy**     | 0.756968535964521  | 0.756968535964521  | 0.756968535964521  | 
 **Macro avg**    | 0.7571854675300642 | 0.756949149356503  | 0.7569076669366066 |         
 **Weighted avg** | 0.757176123824854  | 0.756968535964521  | 0.7569126939309516 |         
          

The RF also performed quite well and provided a respectable over 75 percent values in all classification report scores.
    """)
