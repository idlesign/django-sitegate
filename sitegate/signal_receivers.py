# -*- coding: utf-8 -*-


def process_email_change(sender, confirmation_domain, code, decrypted_data, request, *args, **kwargs):
    from sitegate.models import EmailConfirmation
    if confirmation_domain == 'email_change':
        if decrypted_data.get('next_step') == 'continue_email_change':
            EmailConfirmation.continue_email_change(
                code, decrypted_data, send_email=True, request=request
            )
        elif decrypted_data.get('next_step') == 'finish_email_change':
            EmailConfirmation.finish_email_change(
                code, decrypted_data, send_email=True, request=request
            )
