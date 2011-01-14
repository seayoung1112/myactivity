from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
import settings

class MyDateTimeWidget(forms.DateTimeInput):
    class Media:
        css = {'all': (settings.MEDIA_URL + "css/widget/datetime.css",),}
        js = (settings.MEDIA_URL + "js/widget/jquery-ui-timepicker-addon.js",
              settings.MEDIA_URL + "js/widget/datetime.js",)
    def __init__(self, attrs={}, format=None):
        super(MyDateTimeWidget, self).__init__(attrs={'class': 'vDateTimeField', 'size': '15'}, format=format)

class MyTimeWidget(forms.TimeInput):
    class Media:
        css = {'all': (settings.MEDIA_URL + "css/widget/datetime.css",),}
        js = (settings.MEDIA_URL + "js/widget/jquery-ui-timepicker-addon.js",
              settings.MEDIA_URL + "js/widget/datetime.js",)
    def __init__(self, attrs={}, format=None):
        super(MyTimeWidget, self).__init__(attrs={'class': 'vTimeField', 'size': '15'}, format=format)

class MySplitDateTime(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        widgets = [MyDateWidget, MyTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(u'<p class="datetime">%s %s<br />%s %s</p>' % \
            (_('Date:'), rendered_widgets[0], _('Time:'), rendered_widgets[1]))