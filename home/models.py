# from django.db import models

# class ZaloToken(models.Model):
#     access_token = models.CharField(max_length=255)
#     refresh_token = models.CharField(max_length=255)    # Optional if needed

# def save_tokens(access_token, refresh_token=None):  # Handle optional refresh token
#         token_obj, created =  ZaloToken.objects.get_or_create(
#             defaults={'access_token': access_token, 'refresh_token': refresh_token}
#         )

# def get_access_token():
#         try:
#             token_obj =  ZaloToken.objects.get()
#             return token_obj.access_token
#         except ZaloToken.DoesNotExist:
#             # Handle situation where token is not found
#             return None

# def get_refresh_token():
#         try:
#             token_obj = ZaloToken.objects.get()
#             return token_obj.refresh_token
#         except ZaloToken.DoesNotExist:
#             # Handle situation where token is not found
#             return None