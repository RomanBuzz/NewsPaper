from django import template


register = template.Library()

# Префиксы нежелательных слов с маленькой буквы:
censor_word = [
    "хуй", "хуя", "хуе", "хуё",
    "бляд",
    "пизд", "пезд", "пёзд",
    "пидор",
]


@register.filter()
def censor(value):
    text = str(value)
    for word in text.split():
        for cw in censor_word:
            if cw in word.lower():
                text = text.replace(word, word[0]+"*"*(len(word)-1), 1)

    return f'{text}'


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()
