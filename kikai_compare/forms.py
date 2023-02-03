from django import forms


class InputForm(forms.Form):

    # Radio buttons for the translation direction
    direction = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[
            ("Ja>En", "Japanese to English"),
            ("En>Ja", "English to Japanese"),
        ],
        initial="Ja>En",
    )

    # Text area for inputting the source text to be translated
    source_text = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        strip=True,
    )
