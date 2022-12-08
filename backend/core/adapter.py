#
# class MySocialAccountAdapter(DefaultSocialAccountAdapter):
#     def authentication_error(self, request, provider_id, error, exception, extra_context):
#         print(provider_id)
#         print(error.__str__())
#         print(exception.__str__())
#         print(extra_context)
#
#     def pre_social_login(self, request, sociallogin):
#         """
#         Invoked just after a user successfully authenticates via a
#         social provider, but before the login is actually processed
#         (and before the pre_social_login signal is emitted).
#
#         We're trying to solve different use cases:
#         - social account already exists, just go on
#         - social account has no email or email is unknown, just go on
#         - social account's email exists, link social account to existing user
#         """
#         # Ignore existing social accounts, just do this stuff for new ones
#         if sociallogin.is_existing:
#             return
#
#         # some social logins don't have an email address, e.g. facebook accounts
#         # with mobile numbers only, but allauth takes care of this case so just
#         # ignore it
#         # some social logins don't have an email address
#         if not sociallogin.email_addresses:
#             return
#
#         if 'email' not in sociallogin.account.extra_data:
#             return
#
#         # find the first verified email that we get from this sociallogin
#         verified_email = None
#         for email in sociallogin.email_addresses:
#             if email.verified:
#                 verified_email = email
#                 break
#
#         # no verified emails found, nothing more to do
#         if not verified_email:
#             return
#
#         # check if given email address already exists as a verified email on
#         # an existing user's account
#         try:
#             existing_email = EmailAddress.objects.get(email__iexact=email.email, verified=True)
#         except EmailAddress.DoesNotExist:
#             # easy fast fix
#             raise ImmediateHttpResponse(redirect('/accounts/login'))
#             return
#
#         # if it does, bounce back to the login page
#         # account = User.objects.get(email=email).socialaccount_set.first()
#         # messages.error(request, "A "
#         #                + account.provider.capitalize() + " account already exists associated to " +
#         #                email_address.email + ". Log in with that instead, and connect your " +
#         #                sociallogin.account.provider.capitalize() +
#         #                " account through your profile page to link them together.")
#         # raise ImmediateHttpResponse(redirect('/accounts/login'))
#
#         # if it does, connect this new social login to the existing user
#         # I can do this, because when user is created in standard way, i'am using email verification -> then i know,
#         # they cannot bypass email address.
#         sociallogin.connect(request, existing_email.user)
