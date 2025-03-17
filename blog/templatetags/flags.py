from django import template

register = template.Library()

def country_flag_emoji(country_code):
    """Convert country code to emoji flag"""
    return ''.join(chr(127397 + ord(c)) for c in country_code.upper())

register.filter('flag_emoji', country_flag_emoji)
