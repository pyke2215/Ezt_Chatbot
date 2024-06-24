from django.db import models

class ZaloToken(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)    # Optional if needed

def save_tokens(access_token, refresh_token=None):  # Handle optional refresh token
        token_obj, created =  ZaloToken.objects.get_or_create(
            defaults={'access_token': access_token, 'refresh_token': refresh_token}
        )

def get_access_token():
        try:
            token_obj =  ZaloToken.objects.get(pk = 1)
            return token_obj.access_token
        except ZaloToken.DoesNotExist:
            # Handle situation where token is not found
            return None

def get_refresh_token():
        try:
            token_obj =  ZaloToken.objects.get(pk = 1)
            return token_obj.refresh_token
        except ZaloToken.DoesNotExist:
            # Handle situation where token is not found
            return None

def updateToken(newAccessToken, newRefreshToken):
    try:
        token_obj =  ZaloToken.objects.filter(pk = 1)
        if token_obj:
            token_obj.update(
            access_token = newAccessToken,
            refresh_token = newRefreshToken
            )
            print("update token and refresh token successfully")
            return token_obj
        if token_obj.DoesNotExist:
            token_obj = ZaloToken.objects.create()
            token_obj.access_token = newAccessToken
            token_obj.refresh_token = newRefreshToken
        return token_obj        
    except ZaloToken.DoesNotExist:
         return None