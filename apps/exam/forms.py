from django import forms


class OrientationForm(forms.Form):
    q_1 = forms.CharField(label="1.  I am very good at giving directions.")
    q_2 = forms.CharField(label="2. I have a poor memory for where I left things.")
    q_3 = forms.CharField(label="3. I am very good at judging distances.")
    q_4 = forms.CharField(label="4. My 'sense of direction' is very good.")
    q_5 = forms.CharField(label="5. I tend to think of my environment in terms of cardinal directions (N, S, E, W).")
    q_6 = forms.CharField(label="6. I very easily get lost in a new city.")
    q_7 = forms.CharField(label="7. I enjoy reading maps.")
    q_8 = forms.CharField(label="8. I have trouble understanding directions.")
    q_9 = forms.CharField(label="9. I am very good at reading maps.")
    q_10 = forms.CharField(label="10. I don't remember routes very well while riding as a passenger in a car.")
    q_11 = forms.CharField(label="11. I don't enjoy giving directions.")
    q_12 = forms.CharField(label="12. It's not important to me to know where I am.")
    q_13 = forms.CharField(label="13. I usually let someone else do the navigational planning for long trips.")
    q_14 = forms.CharField(label="14. I can usually remember a new route after I have traveled it only once.")
    q_15 = forms.CharField(label="15. I don't have a very good 'mental map' of my environment.")
