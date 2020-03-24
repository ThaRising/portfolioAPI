# !python3
# -*- coding: utf-8 -*-

from application import create_app

app = create_app()
host = "0.0.0.0"

if __name__ == "__main__":
    app.run(host=host)
