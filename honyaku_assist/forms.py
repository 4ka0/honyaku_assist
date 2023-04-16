from django import forms


class InputForm(forms.Form):

    # Text area for inputting the source text to be translated
    source_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8, 'autofocus': True}),
        max_length=1000,
        strip=True,
        label=False,
    )

    # Radio buttons for the translation direction
    translation_direction = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[
            ("Ja>En", "Japanese to English"),
            ("En>Ja", "English to Japanese"),
        ],
        initial="Ja>En",
        label=False,
    )
