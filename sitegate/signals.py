"""This file contains signals emitted by sitegate."""
import django.dispatch

# Emitted when user successfully signs up.
sig_user_signup_success = django.dispatch.Signal(providing_args=['signup_result', 'flow', 'request'])

# Emitted when user sign up fails.
sig_user_signup_fail = django.dispatch.Signal(providing_args=['signup_result', 'flow', 'request'])
