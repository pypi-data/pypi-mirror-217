from veloweb import velo

app = velo()

@app.route('/', secure=True, methods=['POST'])
async def home(request):
    return app.make_response("Welcome to home page")

if __name__ == '__main__':
    app.runserver()