Git Achievements
===================

## What	is Git-Achievements
Git Achievements is a service-based hook for Github and Bitbucket that allows developers, designers and program managers alike to record all the achievements they acquire, their colleagues, or just random strangers whom they're secretly stalking. Compete against friend and foe alike, or just have fun using the service. After an event is executed on the respective services, the web-hook service activates and pushes to our service's endpoint to let us know what happened.

## Getting Started
1.  Follow the steps for adding a web-hook on Github: [Setting up a hook](http://developer.github.com/webhooks/creating/#setting-up-a-webhook)
2.  For the endpoint, put in `www.git-achievements.com/hook/web`
3.  Login to the site (OAuth with Github) to check your achievements and progress.

## Local Setup
1. Download the project and deploy it to your local server.
2. Run `pip install -r requirements.txt`, in a [virtual environment](http://www.virtualenv.org/en/latest/virtualenv.html) or otherwise
3. Run `python manage.py runserver 0.0.0.0:3000`
4. Follow the steps in the [Getting Started](#getting-started) section, but put the endpoint as `your-local-server/hook/web`

## Contributing
Will add guidelines and best practices eventually.

## License
http://ford.mit-license.org

###The MIT License (MIT)
Copyright © 2014 Ford Peprah <ford.peprah@uwaterloo.ca>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of t\
he Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN \
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
