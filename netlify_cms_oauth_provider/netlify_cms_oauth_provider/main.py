import json
from pathlib import Path


from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from mangum import Mangum
from requests_oauthlib import OAuth2Session



from netlify_cms_oauth_provider.settings import settings

app = FastAPI()

client_id = settings.OAUTH_CLIENT_ID
client_secret = settings.OAUTH_CLIENT_SECRET
authorization_base_url = "https://github.com/login/oauth/authorize"
token_host = settings.GIT_HOSTNAME
token_path = settings.OAUTH_TOKEN_PATH
authorize_path = settings.OAUTH_AUTHORIZE_PATH
token_url = "{token_host}{token_path}".format(
    token_host=token_host, token_path=token_path
)
scope = settings.SCOPES

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@app.get("/auth", response_class=RedirectResponse)
def auth():
    """We clicked login now redirect to github auth"""
    oauth2_session = OAuth2Session(client_id, scope=scope)
    authorization_url, _ = oauth2_session.authorization_url(authorization_base_url)
    return RedirectResponse(authorization_url)


@app.get("/callback", response_class=HTMLResponse)
def callback(request: Request, state: str):
    """retrieve access token"""
    try:
        github = OAuth2Session(client_id, state=state, scope=scope)
        token = github.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=str(request.url),
        )
        content = json.dumps(
            {"token": token.get("access_token", ""), "provider": "github"}
        )
        message = "success"
    except BaseException as e:
        message = "error"
        content = str(e)
    post_message = json.dumps("authorization:github:{0}:{1}".format(message, content))
    return templates.TemplateResponse(
        "callback.html", {"request": request, "post_message": post_message}
    )


@app.get("/success")
def success():
    return Response("", 204)


handler = Mangum(app)
