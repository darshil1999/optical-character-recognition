from django import forms
from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text="Enter your email address.")
    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            if field.help_text:
                field.widget.attrs.update({'placeholder': field.help_text})

            field.help_text = None


class ImageUploadForm(forms.Form):
    file = forms.FileField(label='Select a file to upload')
    LANGUAGE_CHOICES = (
    ('abq', 'Abaza'),
    ('ady', 'Adyghe'),
    ('af', 'Afrikaans'),
    ('ang', 'Angika'),
    ('ar', 'Arabic'),
    ('as', 'Assamese'),
    ('ava', 'Avar'),
    ('az', 'Azerbaijani'),
    ('be', 'Belarusian'),
    ('bg', 'Bulgarian'),
    ('bh', 'Bihari'),
    ('bho', 'Bhojpuri'),
    ('bn', 'Bengali'),
    ('bs', 'Bosnian'),
    ('ch_sim', 'Simplified Chinese'),
    ('ch_tra', 'Traditional Chinese'),
    ('che', 'Chechen'),
    ('cs', 'Czech'),
    ('cy', 'Welsh'),
    ('da', 'Danish'),
    ('dar', 'Dargwa'),
    ('de', 'German'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('et', 'Estonian'),
    ('fa', 'Persian (Farsi)'),
    ('fr', 'French'),
    ('ga', 'Irish'),
    ('gom', 'Goan Konkani'),
    ('hi', 'Hindi'),
    ('hr', 'Croatian'),
    ('hu', 'Hungarian'),
    ('id', 'Indonesian'),
    ('inh', 'Ingush'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('kbd', 'Kabardian'),
    ('kn', 'Kannada'),
    ('ko', 'Korean'),
    ('ku', 'Kurdish'),
    ('la', 'Latin'),
    ('lbe', 'Lak'),
    ('lez', 'Lezghian'),
    ('lt', 'Lithuanian'),
    ('lv', 'Latvian'),
    ('mah', 'Magahi'),
    ('mai', 'Maithili'),
    ('mi', 'Maori'),
    ('mn', 'Mongolian'),
    ('mr', 'Marathi'),
    ('ms', 'Malay'),
    ('mt', 'Maltese'),
    ('ne', 'Nepali'),
    ('new', 'Newari'),
    ('nl', 'Dutch'),
    ('no', 'Norwegian'),
    ('oc', 'Occitan'),
    ('pi', 'Pali'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('rs_cyrillic', 'Serbian (cyrillic)'),
    ('rs_latin', 'Serbian (latin)'),
    ('sck', 'Nagpuri'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('sq', 'Albanian'),
    ('sv', 'Swedish'),
    ('sw', 'Swahili'),
    ('ta', 'Tamil'),
    ('tab', 'Tabassaran'),
    ('te', 'Telugu'),
    ('th', 'Thai'),
    ('tjk', 'Tajik'),
    ('tl', 'Tagalog'),
    ('tr', 'Turkish'),
    ('ug', 'Uyghur'),
    ('uk', 'Ukranian'),
    ('ur', 'Urdu'),
    ('uz', 'Uzbek'),
    ('vi', 'Vietnamese'))
    
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, label='Select language')