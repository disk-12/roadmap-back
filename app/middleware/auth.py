from typing import Union

from fastapi import Response, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth


# Bearer ヘッダーを検証し ID を返却
def auth_user(
        res: Response,
        cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
) -> str:
    user_id = get_user_id(res, cred)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )

    return user_id


# 認証をせずに uid を取得したい場合のみ使用する
def get_user_id(
        res: Response,
        cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
) -> Union[str, None]:
    if cred is None:
        return None

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
