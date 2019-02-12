from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, JSONResponse
from websockets.exceptions import ConnectionClosed
import uvicorn
import asyncio
from coolname import generate_slug
import json


app = Starlette(debug=True, template_directory='templates')

VOTES = []
CLIENTS = []

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

@app.websocket_route('/receive')
async def receive(ws):
    await ws.accept()

    name = generate_slug(2)
    CLIENTS.append(name)
    try:
        while ws.client_state.CONNECTED and ws.application_state.CONNECTED:
            await ws.send_text(json.dumps({
                'me': name,
                'total': sum(VOTES),
                'everyone': CLIENTS
            }))
            await asyncio.sleep(1)
    except ConnectionClosed:
        pass
    CLIENTS.remove(name)
    await ws.close()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

