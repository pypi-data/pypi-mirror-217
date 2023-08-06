At the moment, our code is capable of storing the files in the database. However, this is not a desirable practice. With time our database will get "fat" and slow, and we do not want that to happen. Images haven't been stored in databases as blobs for a while now, and you'll typically save images on your own server where the application is hosted on, or on an external server or service such as AWS's S3.

Multiple file input 
from django.forms import ModelForm, ClearableFileInput
from .models import Beast

class BeastForm(ModelForm):
    class Meta: 
        model = Beast
		fields = '__all__'
        widgets = {
            'media': ClearableFileInput(attrs={'multiple': True})
        }

# 