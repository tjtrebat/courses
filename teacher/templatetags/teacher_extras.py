from django import template
from django.template import Context
from django.core.urlresolvers import reverse

register = template.Library()

class SortableNode(template.Node):
    def __init__(self, viewname):
        self.viewname = viewname
    def render(self, context):
        t = template.loader.get_template('teacher/_sortable.html')
        return t.render(Context({'url': reverse(self.viewname)}, autoescape=False))

@register.tag
def do_sortable(parser, token):
    contents = token.contents.split(None)
    try:
        tag_name, viewname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % contents[0])
    if not (viewname[0] == viewname[-1] and viewname[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return SortableNode(viewname.replace('"', "").replace("'", ""))

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
    for i, id in enumerate(ids):
        if not (id[0] == id[-1] and id[0] in ('"', "'")):
            raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
        ids[i] = id.replace('"', "").replace("'", "")
    return DatetimeNode(ids)

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
    for i, id in enumerate(ids):
        if not (id[0] == id[-1] and id[0] in ('"', "'")):
            raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
        ids[i] = id.replace('"', "").replace("'", "")
    return TabsNode(ids)