import jinja2
import aiohttp_jinja2
from aiohttp import web

import workwithbase


ip_addr = '0.0.0.0'
port = 80


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
        return aiohttp_jinja2.render_template('mistake.html', request, {'text': "You have to sign in first!"})
    return {}


async def handle_login(request):
    data = await request.post()
    login = data['login']
    password = data['password']
    result = workwithbase.auth_user(login, password)
    if result:
        response = web.HTTPFound('/')
        response.set_cookie("nickname", result[0])
        response.set_cookie("hash", "hash6456")
        return response
    return aiohttp_jinja2.render_template('index.html', request, {'mistake_auth': 'Неверные данные'})


async def handle_signup(request):
    data = await request.post()
    
    login = data['Login']
    email = data['Email']
    password = data['Password']
    phone = data['Phone']
    age = data['Age']
    sex = data['genderRadios']
    
    result = workwithbase.add_user(login, password, email, phone, age, sex)
    if result == 0:
        return aiohttp_jinja2.render_template('registration.html', request, {"phone": phone, "age": age, "email": email, "mistake_login": "Этот логин занят"})
    elif result == 1:
        return aiohttp_jinja2.render_template('registration.html', request, {"phone": phone, "age": age, "login": login, "mistake_email": "Этот e-mail занят"})
    else:
        response = web.HTTPFound('/')
        response.set_cookie("nickname", result[0])
        response.set_cookie("hash", "hash6456")
        return response
    

async def handle_logout(request):
    response = web.HTTPFound('/')
    response.del_cookie("nickname")
    return response


async def handle_404(request):
    name = request.match_info.get('tail', "kek")
    text = "404: " + name + " not found"
    return aiohttp_jinja2.render_template('mistake.html', request, {'text': text})


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
app.router.add_get('/mistake{text}', handle_info)

web.run_app(app, host=ip_addr, port=port)
