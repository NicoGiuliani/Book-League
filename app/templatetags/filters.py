from django import template

register = template.Library()

@register.filter(name="preview")
def preview(value, max_words):
    word_list = value.split(" ")
    if len(word_list) > max_words:
        preview_words = word_list[0:max_words]
        return " ".join(preview_words) + "..."
    return value

register.filter("preview", preview)