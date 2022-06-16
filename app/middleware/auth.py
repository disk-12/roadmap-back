from fastapi import Response, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth


# Bearer ヘッダーを検証し Firebase User を返
def get_user_id(res: Response,
                cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> dict:
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )

    try:
        from app.main import get_settings

        if cred.credentials == get_settings().dummy_uid:
            decoded_token = {
                'uid': get_settings().dummy_uid
            }
        else:
            decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )

    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return decoded_token['uid']
