import os
import discord
import requests
from dotenv import load_dotenv
from backend.bots.ntm_dev import bot as ntmdev
from quart import Quart, redirect, request, session, render_template, send_from_directory, Blueprint

app = Quart(__name__, static_folder='site/static', template_folder='site/templates')
routes = Blueprint('routes', __name__)

load_dotenv()

# Configurações do Discord
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://ntm-dev-web.onrender.com/discord/callback"

@routes.route('/site/templates/<path:filename>')
async def templates_path(filename):
    return await send_from_directory('site/templates', filename)

@routes.route('/site/static/<path:filename>')
async def static_files(filename):
    return await send_from_directory('site/static', filename)

@routes.route("/")
async def home():
    if "user_id" in session:
        username = session["username"]
        avatar_url = session["avatar_url"]
        return await render_template("index-PT.html", username=username, avatar_url=avatar_url)
    return await render_template("login-PT.html")

@routes.route("/discord/login")
async def login():
    return redirect(f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify")

@routes.route("/discord/callback")
async def callback():
    code = request.args.get("code")
    if not code:
        return "Erro ao autenticar: código ausente.", 400

    # Trocar o código por um token de acesso
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)

    if response.status_code != 200:
        print("Erro ao obter token:", response.text)
        return "Erro ao obter token. Verifique as configurações.", 400

    token = response.json().get("access_token")
    if not token:
        return "Erro ao obter o token de acesso.", 400

    # Obter informações do usuário
    user_response = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {token}"},
    )
    if user_response.status_code != 200:
        return "Erro ao obter dados do usuário.", 400

    user_data = user_response.json()
    user_id = user_data["id"]
    username = user_data["username"]
    discriminator = user_data["discriminator"]
    avatar_hash = user_data["avatar"]

    # Construir a URL do avatar
    if avatar_hash:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"
    else:
        avatar_url = f"https://cdn.discordapp.com/embed/avatars/{int(discriminator) % 5}.png"

    # Armazenar na sessão
    session["user_id"] = user_id
    session["username"] = username
    session["avatar_url"] = avatar_url

    # Redirecionar para a página index
    return redirect("/")

@routes.route("/login-PT")
async def login_PT():
    return await render_template("login-PT.html")

@routes.route("/login-US")
async def login_US():
    return await render_template("login-US.html")


@routes.route("/index-PT")
async def index_PT():
    if "user_id" in session:
        username = session["username"]
        avatar_url = session["avatar_url"]
        return await render_template("index-PT.html", username=username, avatar_url=avatar_url)
    return redirect("/")

@routes.route("/index-US")
async def index_US():
    if "user_id" in session:
        username = session["username"]
        avatar_url = session["avatar_url"]
        return await render_template("index-US.html", username=username, avatar_url=avatar_url)
    return redirect("/")


@routes.route("/change_language")
async def change_language():
    language = request.args.get('lang')
    if language == "US":
        return redirect("/index-US")
    else:
        return redirect("/index-PT")

@routes.route("/change_language_login")
async def change_language_login():
    language = request.args.get('lang')
    if language == "US":
        return redirect("/login-US")
    else:
        return redirect("/login-PT")

@routes.route("/comprar", methods=["POST"])
async def comprar():
    if "user_id" not in session:
        return {"success": False, "message": "Usuário não autenticado."}, 401

    user_id = int(session["user_id"])
    user = ntmdev.get_user(user_id)

    if not user:
        try:
            user = await ntmdev.fetch_user(user_id)
        except discord.NotFound:
            return {"success": False, "message": "Usuário não encontrado no Discord."}, 404
        except discord.HTTPException as e:
            return {"success": False, "message": "Erro ao buscar usuário no Discord."}, 500

    try:
        mensagem = f"Olá, {session['username']}! Para fazer a compra do produto entre no nosso discord, https://discord.gg/aKpwVrXgyx e abra um ticket em https://discord.com/channels/1290074291047632919/1303725153934381090. Se tiver dúvidas, entre em contato com nossa equipe de suporte."
        await user.send(mensagem)
        return {"success": True, "message": "Mensagem enviada com sucesso."}, 200
    except discord.Forbidden:
        return {"success": False, "message": "Não foi possível enviar mensagem. O usuário pode ter bloqueado mensagens diretas."}, 403
    except discord.HTTPException as e:
        print(f"Erro ao enviar mensagem para {user_id}: {e}")
        return {"success": False, "message": "Erro ao enviar a mensagem."}, 500

@routes.route("/buy", methods=["POST"])
async def buy():
    if "user_id" not in session:
        return {"success": False, "message": "User not authenticated."}, 401

    user_id = int(session["user_id"])
    user = ntmdev.get_user(user_id)

    if not user:
        try:
            user = await ntmdev.fetch_user(user_id)
        except discord.NotFound:
            return {"success": False, "message": "User not found on Discord."}, 404
        except discord.HTTPException as e:
            return {"success": False, "message": "Error fetching user on Discord."}, 500

    try:
        message = (
            f"Hello, {session['username']}! To purchase the product, join our Discord at https://discord.gg/aKpwVrXgyx and open a ticket at "
            "https://discord.com/channels/1290074291047632919/1303725153934381090. If you have any questions, please contact our support team."
        )
        await user.send(message)
        return {"success": True, "message": "Message sent successfully."}, 200
    except discord.Forbidden:
        return {"success": False, "message": "Could not send message. The user may have blocked direct messages."}, 403
    except discord.HTTPException as e:
        print(f"Error sending message to {user_id}: {e}")
        return {"success": False, "message": "Error sending the message."}, 500

@routes.route("/logout")
async def logout():
    session.clear()
    return redirect("/")
