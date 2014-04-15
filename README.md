Git Achievements
===================

## What I've Learned
Even after deploying a site and `Flask` application prior, deploying a Django application is a whole different mess of problems.  The following two resources provide excellent information on how to get up and running with your Django application:
* [Digital Ocean's Configuring Nginx, Gunicorn and Django](https://www.digitalocean.com/community/articles/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn)
* [Michal Karzynski's Django, Nginx, Gunicorn, Virtualenv, and Supervisor](http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/)
Besides those two guides, if you're familiar with setting up a Django application on your server, the steps to getting your own local instance up and running aren't that bad:
1. Set up a virtual environment for the project.
2. Run `pip install -r requirements/web.txt` to install the web requirements
3. You need to have `psycopg2`, `python-dev` and `nginx` installed which you should have from prior steps (if on Mac, you can replace `sudo apt-get install` with `brew install` using [brew](http://brew.sh/)).
4. Generate a secret key/id pair by [registering a new application on Github](https://github.com/settings/applications/new).
5. Copy the `samples/settings/custom.py` settings file to `gitachievements/settings/custom.py` and fill it in the with the relevant information you obtained from the above steps.
6. Run `python manage.py syncdb` to load in the events, and if you want to have initial data, then run `python loaddata.py` as well.
7. A convenience script in included in `samples/bin` called `gunicorn_start`, you can fill that in and give it as passenger's command.


## Contributors
[Ford P, hkpeprah](https://github.com/hkpeprah) - Code + Design  
[Nicholas Terwoord, nt3rp](https://github.com/nt3rp) - Idea  
[Brian L, 1337](https://github.com/1337) - Code + Idea  
  

## License
http://ford.mit-license.org

###The MIT License (MIT)
Copyright © 2014 Ford Peprah <ford.peprah@uwaterloo.ca>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of t\
he Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN \
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

