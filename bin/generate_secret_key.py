#!/usr/bin/env python
from django.utils.crypto import get_random_string


if __name__ == "__main__":
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    print get_random_string(50, chars)
