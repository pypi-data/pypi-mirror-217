# Flask-Tunnel

> A minor improvement on the [flask-ngrok](https://pypi.org/project/flask-ngrok/) tool for tunneling [Flask](https://flask.palletsprojects.com/en/2.3.x/) web apps to public URLs. Added support for [ngrok](https://ngrok.com/) configs, such as authentication, custom domains, and logging; can run on Jupyter clients such as [Google Colab](https://colab.google/).

## Installation

```bash
pip install flask-tunnel
```

## Example

```py
from flask import Flask
from flask_tunnel import FlaskTunnel

app = Flask(__name__)
FlaskTunnel(app, auth="#####", subdomain="flask-tunnel")

@app.route("/")
def hello():
    return "Hello World"

app.run(port=5000)
```

For details on using the `config` parameter of `FlaskTunnel`, see pyngrok's [documentation](https://pyngrok.readthedocs.io/en/latest/api.html#pyngrok.conf.PyngrokConfig) on `PyngrokConfig`. 

## License

[MIT](LICENSE)