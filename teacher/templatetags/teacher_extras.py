from django import template
from django.template import Context

register = template.Library()

class DatetimeNode(template.Node):
    def __init__(self, ids):
        self.ids = ids
    def render(self, context):
        t = template.loader.get_template('teacher/_datetime.html')
        return t.render(Context({'ids': self.ids}, autoescape=False))

@register.tag
def do_datetime(parser, token):
    contents = token.contents.split(None)
    try:
        tag_name, ids = contents[:1], contents[1:]
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % contents[0])

    return DatetimeNode(["#%s" % i for i in ids])

class TabsNode(template.Node):
    def __init__(self, ids):
        self.ids = ids
    def render(self, context):
        t = template.loader.get_template('teacher/_tabs.html')
        return t.render(Context({'ids': self.ids}, autoescape=False))

@register.tag
def do_tabs(parser, token):
    contents = token.contents.split(None)
    try:
        tag_name, ids = contents[:1], contents[1:]
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % contents[0])

    return TabsNode(["#%s" % i for i in ids])