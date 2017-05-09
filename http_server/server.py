
import jinja2
import aiohttp_jinja2
from aiohttp import web

import workwithbase

@aiohttp_jinja2.template('index.html')
async def handle_index(request):
    login = request.cookies.get("nickname", '')
    if not login:
        return {}
    return {"login": login}

async def handle_login(request):
    data = request.query
    email = data.get('email')
    password = data.get('password')
    result = workwithbase.auth_user(email, password)
    if result:
        response = web.HTTPFound('/info')
        response.set_cookie("nickname", result[0])
        response.set_cookie("hash", "hash6456")
        return response
    return web.Response(text='invalid login')


@aiohttp_jinja2.template('info.html')
async def handle_info(request):
    if request.cookies.get("nickname", "") == "":
        return web.Response(text="You have to sign in first!")
    return {}


@aiohttp_jinja2.template('registration.html')
async def handle_registration(request):
    return {}


async def handle_signup(request):
    data = request.query
    login = data.get('Login')
    name = data.get('Name')
    email = data.get('Email')
    password = data.get('Password')
    confirm_password = data.get('confirmPassword')
    phone = data.get('Phone')
    age = data.get('Age')
    sex = data.get('genderRadios')
    agree = data.get('Agree')
    if agree and (password == confirm_password):
        result = workwithbase.add_user(login, password, name, email, phone, age, sex)
    else: 
        return web.Response(text="invalid passwords or u don't agree")
    if result:
        response = web.HTTPFound('/info')
        response.set_cookie("nickname", result[0])
        response.set_cookie("hash", "hash6456")
        return response
    return web.Response(text='invalid login or e-mail')
    

async def handle_logout(request):
    name = request.cookies.get("nickname", "")
    response = web.Response(text="Goodbye, {}!".format(name))
    response.del_cookie("nickname")
    return response


async def handle_404(request):
    name = request.match_info.get('tail', "kek")
    text = "404: " + name + " not found"
    return web.Response(text=text)


app = web.Application()

aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('front_server', "templates"))


app.router.add_static('/static', 'front_server/static', name='static')


app.router.add_get('/', handle_index)
app.router.add_get('/login', handle_login)
app.router.add_get('/registration', handle_registration)
app.router.add_get('/sign_up', handle_signup)
app.router.add_get('/logout', handle_logout)
app.router.add_get('/info', handle_info)
app.router.add_get('/{tail:.*}', handle_404)

web.run_app(app, host='0.0.0.0', port=8080)
