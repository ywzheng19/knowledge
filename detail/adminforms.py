from django import forms
from ckeditor.widgets import CKEditorWidget

class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='描述', required=False)
    content = forms.CharField(widget=CKEditorWidget(), label='正文', required=True)


class LogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label='更新内容', required=True)
