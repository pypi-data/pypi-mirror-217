# MEdit - Markup Editor


## Installation

```sh
[<PYTHON> -m] pip[3] install [--upgrade] medit
```


## Usage


## Development & Contribution

```sh
pip3 install -U poetry pre-commit
git clone --recurse-submodules https://projects.om-office.de/frans/pocketrockit.git
cd pocketrockit
pre-commit install
# if you need a specific version of Python inside your dev environment
poetry env use ~/.pyenv/versions/3.10.4/bin/python3
poetry install
```

After modifications, this way a newly built wheel can be checked and installed:

```sh
poetry build
poetry run twine check dist/pocketrockit-0.0.25-py3-none-any.whl
python3 -m pip install --user --upgrade dist/pocketrockit-0.0.25-py3-none-any.whl
```

## 1.0 TODO

* [ ] Show local images
* [ ] Show remote images
* [ ] File to title
* [ ] proper Qt style
* [ ] slim file / folder create / rename
* [ ] proper View CSS selector
* [ ] File viewer for Plain, Python, YAML, JSON, ..
* [ ] Autoload
* [ ] Save
* [ ] View follows editor
* [ ] Links clickable
* [ ] Fix Links to support `(text)[url]` syntax


## Feature ideas

* [ ] export to Pdf / Html / docx ..
* [ ] copy / paste images
* [ ] drag & drop images
* [ ] spell checker


## Read

https://github.com/sindresorhus/github-markdown-css
https://python-markdown.github.io/extensions/code_hilite/#step-1-download-and-install-pygments
https://github.com/richleland/pygments-css
https://github.com/OzakIOne/markdown-github-dark
https://github.com/jamiemcg/remarkable
https://github.com/sindresorhus/github-markdown-css

https://thomasf.github.io/solarized-css/
https://thomasf.github.io/solarized-css/solarized-light.css

https://markdowncss.github.io/
https://github.com/markdowncss/retro

https://mixu.net/markdown-styles/

https://github.com/altercation/solarized

https://www.jsdelivr.com/package/npm/@naokim03/markdown-theme-solarized