from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Any
from app.db.supabase import SUPABASE

bearer_scheme = HTTPBearer()


def check_login(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> bool:
    client = SUPABASE().client
    try:
        response = client.auth.get_user(token.credentials)

        # Vérification que l'utilisateur existe et n'est pas anonyme
        if response.user is None:
            return False

        # Vérifications supplémentaires optionnelles
        if not response.user.id:
            return False

        # Vérifier si l'email est confirmé (optionnel selon ton besoin)
        if not response.user.email_confirmed_at:
            return False

        return True
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    

def update_session(rtoken: str) -> dict[str, Any]:
    client = SUPABASE().client
    response = client.auth.refresh_session(rtoken)
    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user_id": response.user.id,
        "email": response.user.email,
        "metadata": response.user.user_metadata,
    }