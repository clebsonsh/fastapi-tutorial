from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': 'bug list'}


@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id):
    # fetch comments of blog with id = id
    return {'data': {
        'comments': [1, 2]
    }}


@app.get('/about')
def about():
    return {'data': 'about page'}
