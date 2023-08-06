from pyngrok import ngrok, conf

class FlaskTunnel():
    def __init__(self, app, auth: str = None, config: conf.PyngrokConfig = None, **kwargs):
        ngrok.kill()
        
        if auth is not None:
            ngrok.set_auth_token(auth)
        
        if config is not None:
            conf.set_default(config)

        self.params = kwargs
        self.next = app.run
        app.run = self.run

    def run(self, *args, **kwargs) -> None:
        port = int(kwargs.get('port', 5000))
        self.tunnel = ngrok.connect(port, **self.params)
        print('Public URL: ', self.tunnel.public_url)
        
        self.next(*args, **kwargs)