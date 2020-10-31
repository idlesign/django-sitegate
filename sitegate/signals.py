"""This file contains signals emitted by sitegate."""
import django.dispatch

sig_user_signup_success = django.dispatch.Signal()
"""Emitted when user successfully signs up.
providing_args=['signup_result', 'flow', 'request']

"""

sig_user_signup_fail = django.dispatch.Signal()
"""Emitted when user sign up fails.
providing_args=['signup_result', 'flow', 'request']

"""
