#!/usr/bin/env python

from indie_flask import app

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
