Git Achievements
===================
## Development Setup
1. [Set up a virtual environment](http://virtualenvwrapper.readthedocs.org/en/latest/) for the project.
1. Enable the virtual environment and run `pip install -r requirements/dev.txt` from the project directory.
1. Run `python manage.py syncdb` to load the events and `python manage.py add_sample_data` to load the initial data.
1. Run `python manage.py runserver` to launch the server.
1. Add social auth key/secret pair if you want to login as your Github profile, otherwise you can login via the admin page `/admin`, then navigate to the root.
1. [Set up a watcher to convert all SCSS files to CSS files](http://www.jetbrains.com/webstorm/webhelp/transpiling-sass-less-and-scss-to-css.html#d128011e807).
1. [Download coffee](https://www.npmjs.org/package/coffee-script) and set it as a watcher `coffee -cw app/**/*.coffee` to compile all coffeescript that you may make changes to.

## Getting set up (Production or Team Server)
The following two resources provide excellent information on how to get up and running with your Django application:
* [Digital Ocean's Configuring Nginx, Gunicorn and Django](https://www.digitalocean.com/community/articles/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn)
* [Michal Karzynski's Django, Nginx, Gunicorn, Virtualenv, and Supervisor](http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/)  

Besides those two guides, if you're familiar with setting up a Django application on your server, the steps to getting your own local instance up and running aren't that bad:  

1. [Set up a virtual environment](http://virtualenvwrapper.readthedocs.org/en/latest/) for the project.
1. Run `pip install -r requirements/web.txt` in the virtual environment to install the web requirements
1. You need to have `psycopg2`, `python-dev` and `nginx` installed which you should have from prior steps (if on Mac, you can replace `sudo apt-get install` with `brew install` using [brew](http://brew.sh/)).
1. Generate a secret key/id pair by [registering a new application on Github](https://github.com/settings/applications/new).
1. Copy the `samples/settings/custom.py` settings file to `gitachievements/settings/custom.py` and fill it in the with the relevant information you obtained from the above steps.
1. Run `python manage.py syncdb` to load in the events, and if you want to have initial data, then run `python manage.py add_sample_data` as well.
1. You will need `coffee` and `sass` to compile the `.coffeescript` and `.scss`, you can install coffeescript via [npm](https://www.npmjs.org/package/coffee-script) and sass via [gem](https://rubygems.org/gems/sass)
1. A convenience script in included in `samples/bin` called `gunicorn_start`, you can fill that in and give it as passenger's command.

## Contributing
Contributing to Git Achievements is simple; fork the repository, make your changes, and submit a pull request.  To help your pull request make it easily into the repository, add tests, describe in full what issue your pull request
addresses, and list the major changes.  In addition, we use the following coding style:
* CoffeeScript is indented with `4` spaces as opposed to the traditional 2.
* Camel-casing for CoffeeScript.
* Underscores for function names in Python (e.g. `get_last_object` instead of `getLastObject` or `getlastobject`)
* Avoid JavaScript if at all possible, instead favour CoffeeScript.
* Avoid CSS instead write a SCSS file and include as a mixin (styles should be as specific as possible unless intended to be global).

## Contributors
[Ford P, hkpeprah](https://github.com/hkpeprah) - Code + Design  
[Nicholas Terwoord, nt3rp](https://github.com/nt3rp) - Idea
[Brian L, 1337](https://github.com/1337) - Code + Idea


## License
[GPL v2](LICENSE.md)
