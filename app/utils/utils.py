import os
from uuid import uuid4


def save_image(image, nick):
    path = os.path.join('app', 'static', 'img',
                                'users', nick, 'wishes')
    filename = f"{uuid4()}{os.path.splitext(image.filename)[1]}"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, filename), 'wb') as file:
        file.write(image.read())
    return os.path.join('static', 'img', 'users', nick, 'wishes', filename)