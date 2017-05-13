import jinja2
import aiohttp_jinja2
from aiohttp import web

import workwithbase


ip_addr = '0.0.0.0'
port = 8080


@aiohttp_jinja2.template('index.html')
async def handle_index(request):
    login = request.cookies.get("nickname", '')
    if not login:
        return {}
    return {"login": login}

@aiohttp_jinja2.template('registration.html')
async def handle_registration(request):
    return {}

@aiohttp_jinja2.template('info.html')
async def handle_info(request):
    if request.cookies.get("nickname", "") == "":
        return web.Response(text="You have to sign in first!")
    return {}


async def handle_login(request):
    data = await request.post()
    email = data['email']
    password = data['password']
    result = workwithbase.auth_user(email, password)
    if result:
        response = web.HTTPFound('/')
        response.set_cookie("nickname", result[0])
        response.set_cookie("hash", "hash6456")
        return response
    return web.Response(text='invalid login')


async def handle_signup(request):
    data = await request.post()
    login = data['Login']
    name = data['Name']
    email = data['Email']
    password = data['Password']
    confirm_password = data['confirmPassword']
    phone = data['Phone']
    age = data['Age']
    sex = data['genderRadios']
    agree = data['Agree']
    result = workwithbase.add_user(login, password, name, email, phone, age, sex)
    if result:
        response = web.HTTPFound('/')
        response.set_cookie("nickname", result[0])
        response.set_cookie("hash", "hash6456")
        return response
    return web.Response(text='invalid login or e-mail')
    

async def handle_logout(request):
    response = web.HTTPFound('/')
    response.del_cookie("nickname")
    return response


async def handle_404(request):
    name = request.match_info.get('tail', "kek")
    text = "404: " + name + " not found"
    return web.Response(text=text)


app = web.Application()

aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('front_server', "templates"))

app.router.add_static('/static', 'front_server/static', name='static')

# Routes
app.router.add_get('/', handle_index)
app.router.add_post('/login', handle_login)
app.router.add_get('/registration', handle_registration)
app.router.add_post('/sign_up', handle_signup)
app.router.add_get('/logout', handle_logout)
app.router.add_get('/info', handle_info)
app.router.add_get('/{tail:.*}', handle_404)

web.run_app(app, host=ip_addr, port=port)
