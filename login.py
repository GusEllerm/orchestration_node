from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from config import SECRET_KEY, user_db
from jwt import PyJWTError

import jwt
import datetime

router = APIRouter()

def get_token_from_cookie(request: Request):
    return request.cookies.get("access_token")

# Dummy function to simulate checking if the user is logged in
def is_user_logged_in(token: str = Depends(get_token_from_cookie)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def generate_token(username: str):
    payload = {
        "sub": username, # Subject (usually the user's username or ID)
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1) # Experiation
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def authenticate_user(username: str, password: str):
    user = user_db.get(username)
    if not user or user['password'] != password:
        return False
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if user:
        token = generate_token(form_data.username)
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        # cookie secure=False in http env, when deployed to HTTPS secure=True
        response.set_cookie(key="access_token", value=token, httponly=True, secure=False, samesite='Lax')
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.get("/login", response_class=HTMLResponse)
def login_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
        <div class="login-container">
            <h2 class="login-title">Login</h2>
            <form class="login-form" action="/login" method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """
