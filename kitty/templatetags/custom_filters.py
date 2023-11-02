from django import template

register = template.Library()


# @register.filter
# def is_less_than_zero(value):
#     print(value)
#     try:
#         a = int(value)
#     except ValueError:
#         return False
#     return a < 0

@register.filter
def is_less_than_zero(value):
    # print(len(value))
    try:
        a = int(value[len(value)-1])
        return a < 0
    except ValueError:
        return False
