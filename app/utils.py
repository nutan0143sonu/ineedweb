from django.core.validators import RegexValidator



EMAILREGEX = RegexValidator(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$','Email must contain at least one @ and .')
MOBILEREGEX = RegexValidator(r'^\+?1?\d{9,15}$', 'Mobile number must be integer')
NAMEREGEX = RegexValidator(r'^[a-zA-Z-]+$', 'Only character is allowed')
YEARREGEX = RegexValidator(r'^\+?1?\d{4,5}$', 'Year must be integer')