from django import template

register = template.Library()

@register.filter(name="preview")
def preview(value, max_words):
    word_list = value.split(" ")
    preview_words = word_list[0:max_words]
    return " ".join(preview_words)

register.filter("preview", preview)