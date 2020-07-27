#!/bin/env python
from app import create_app, server

app = create_app()

if __name__ == '__main__':
  app.run_server(debug=True)