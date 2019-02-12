from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, JSONResponse
import uvicorn


app = Starlette(debug=True, template_directory='templates')

VOTES = []

@app.route('/')
async def homepage(request):
    template = app.get_template('index.html')
    content = template.render(request=request)
    return HTMLResponse(content)

@app.route('/vote_total', methods=['GET'])
async def vote_total(request):
    return JSONResponse({'total': sum(VOTES)})

@app.route('/cast_vote', methods=['POST'])
async def cast_vote(request):
    VOTES.append(1)
    return JSONResponse({'status': 'ok'})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

