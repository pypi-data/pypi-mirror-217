#!/usr/bin/env python3

# Copyright (c) 2023 Jeff Dileo.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import argparse
import os
import os.path
import shutil
import toml
from collections.abc import Callable
import chevron
import weasyprint
import markdown # temporary
import subprocess
import io
from bs4 import BeautifulSoup

from .pf import entrypoint

# disable remote url resolution and path traversal
def fetcher(url):
  u = None
  if url.startswith("file://"):
    u = url[7:]
  else:
    u = "./" + url
  cwd = os.path.abspath(".")
  target = os.path.abspath(u)
  if target.startswith(cwd + os.sep):
    return weasyprint.default_url_fetcher("file://" + target)
  else:
    sys.stderr.write("invalid url: " + repr(url) + "\n")
    sys.exit(1)

# disable mustache lambdas. too much magic.
# chevron 0.14.0 only exists on pypi, which is admittedly spooky
# we should dep on 0.13.1 from github or pypi specifically
# but for now we'll mock the 0.14.0 _get_key signature
# which changes wildly between versions
real_get_key = chevron.renderer._get_key
def fake_get_key(key, scopes, warn=None):
  if key.startswith("__") or ".__" in key:
    return ["no soup for you."]
  r = real_get_key(key, scopes, warn=warn)
  if isinstance(r, Callable):
    return ["no soup for you!"]
  return r
chevron.renderer._get_key = fake_get_key
# >>> chevron.render('Hello, {{#mustache}}{{#__class__.__bases__}}{{#__subclasses__}}{{.}}{{/__subclasses__}}{{/__class__.__bases__}}{{/mustache}}!', {'mustache': 'World'})
# 'Hello, no soup for you.!'
# >>> chevron.render('Hello, {{#mustache}}{{#upper}}{{.}}{{/upper}}{{/mustache}}!', {'mustache': 'world'})
# 'Hello, no soup for you!!'


footnotecount = 1


def convert(path, opts, toc, args):
  #print("convert(" + repr(path) + ")")
  proc1 = subprocess.run(['pandoc', '-t', 'json', path], capture_output=True)
  if proc1.returncode != 0:
    sys.stderr.write("error running initial pandoc command: \n")
    sys.stderr.buffer.write(proc1.stderr)
    sys.stderr.write("\n")
    sys.exit(1)
  o1 = proc1.stdout.decode('utf-8')

  if args.debug:
    print(o1)

  # run the panflute filter
  sys.argv = ["html"]
  iw = io.StringIO(o1)
  ow = io.StringIO("")

  headers = []
  _headers = []
  r = entrypoint(iw, ow, _headers)
  ow.seek(0)
  o2 = ow.read()

  if len(_headers) == 1:
    headers = _headers[0]

  if "columns" in opts:
    toc.append(opts | {"name": opts['section_name'] + "-columns-title", "issubsection": False})

  #print(repr(headers))
  header_level = int(opts.get('toc_header_level', ['1'])[0])

  for h in headers:
    if h.level <= header_level:
      toc.append(opts | {"name": h.identifier, "issubsection": h.level != 1})

  # pass back to pandoc
  proc2 = subprocess.run(['pandoc', '-f', 'json',
                          '-t', 'html',
                          '--wrap=none'],
                         input=o2, text=True,
                         capture_output=True)
  if proc2.returncode != 0:
    sys.stderr.write("error running initial pandoc command: \n")
    sys.stderr.write(proc2.stderr)
    sys.stderr.write("\n")
    sys.exit(1)
  content = proc2.stdout
  return content


def parse_args():
  parser = argparse.ArgumentParser(
    description='A flexible document generator based on WeasyPrint, mustache templates, and Pandoc.'
  )
  subparsers = parser.add_subparsers(dest='command', required=True,
                                     title='subcommands',
                                     description='valid subcommands',
                                     help='additional help')

  create = subparsers.add_parser('create')
  create.add_argument('project', metavar='<project>', type=str,
                      help="Name of project to create.")
  create.add_argument('-t', '--template', metavar='<path>', type=str,
                      default="",
                      help='Create from alternative template path instead of the built-in default.')
  build = subparsers.add_parser('build')
  parser.add_argument('-d', '--debug', action='store_true',
                      help='Debug output.')
  build.add_argument('config', metavar='<config>', type=str,
                      help="Path to document toml configuration file.")
  args = parser.parse_args()
  return args

def main():
  args = parse_args()

  if args.command == "build":
    build(args)
  elif args.command == "create":
    projpath = args.project
    if os.path.exists(projpath):
      sys.stderr.write(f"error: path '{projpath}' already exists.\n")
      sys.exit(1)
    absprojpath = os.path.abspath(projpath)
    os.makedirs(os.path.dirname(absprojpath), exist_ok=True)

    modpath = os.path.dirname(os.path.abspath(__file__))
    staticpath = os.path.join(modpath, "static")
    templatepath = None
    if args.template == "":
      templatepath = staticpath
    else:
      templatepath = args.template
    shutil.copytree(templatepath, absprojpath)

    projname = os.path.basename(absprojpath)
    if os.path.exists(os.path.join(absprojpath, "project.toml")):
      os.rename(os.path.join(absprojpath, "project.toml"),
                os.path.join(absprojpath, projname + ".toml"))
    else:
      print("project.toml not found in template path " + repr(args.template) + ".... using default.")
      shutil.copyfile(os.path.join(staticpath, "project.toml"),
                os.path.join(absprojpath, projname + ".toml"))

def build(args):
  global footnotecount

  config = args.config
  if not os.path.exists(config):
    sys.stderr.write(f"error: '{config}' not found.\n")
    sys.exit(1)
  if not os.path.isfile(config):
    sys.stderr.write(f"error: '{config}' is not a file.\n")
    sys.exit(1)

  dir, fname = os.path.split(config)
  wd = os.getcwd()
  if dir != "":
    os.chdir(dir)

  config = toml.loads(open(fname, 'r').read())
  config['config'] = config # we occasionally need top.down.variable.paths to resolve abiguity

  base_template = open('templates/base.html', 'r').read()
  section_template = open('templates/section.html', 'r').read()
  toc_template = open('templates/toc.html', 'r').read()

  body = ''

  sections = []
  toc = []

  for section in config['sections']:
    if section['type'] == 'section':
      # markdown
      section_name = section['name']
      section_path = 'sections/{}.md'.format(section['name'])
      content = open(section_path, 'rb').read()
      #print(repr(content))
      content = content.decode('utf-8')
      md = markdown.Markdown(extensions=["meta"])
      html = md.convert(content)
      opts = md.Meta | section
      opts['section_name'] = section_name
      html = convert(section_path, opts, toc, args)
      footnotes = ""
      soup = BeautifulSoup(html, 'html.parser')
      _fns = soup.find(id="footnotes")
      if _fns is not None:
        _fns = _fns.extract()
        _fns.ol['start'] = str(footnotecount)
        _fns.ol['style'] = f"counter-reset:list-item {footnotecount}; counter-increment:list-item -1;"
        __fns = [c for c in _fns.ol.children if c != "\n"]
        footnotecount += len(__fns)
        del _fns['id']
        for __fn in __fns:
          id = __fn['id']
          nid = section_name + "-" + id
          __fn['id'] = nid
          __fnx = soup.find(id=id)
          if __fnx is not None:
            __fnx['id'] = nid
        for _a in soup.find_all(class_="footnote-ref"):
          _a['id'] = section_name + "-" + _a['id']
          _a['href'] = '#' + section_name + "-" + _a['href'][1:]
          print(_a)
        for _a in _fns.find_all(class_="footnote-back"):
          _a['href'] = '#' + section_name + "-" + _a['href'][1:]

        footnotes = str(_fns)
        html = str(soup)

      opts['html'] = html
      opts['footnotes'] = footnotes
      opts['opts'] = opts # we occasionally need top.down.variable.paths to resolve abiguity
      template = section_template
      if "alt" in section:
        template = open('templates/{}.html'.format(section['alt']), 'r').read()
      r = chevron.render(template, opts)
      sections.append(r)
    elif section['type'] == 'toc':
      # defer until after we get through everything else
      sections.append(section)
    else:
      # assume in templates/
      template = open('templates/{}.html'.format(section['type']), 'r').read()
      r = chevron.render(template, config)
      sections.append(r)
      if section['type'] != 'cover' and "title" in section:
        toc.append(opts | {"name": section['type'], "issubsection": False})

  for section in sections:
    if type(section) == str:
      body += section
      body += "\n"
    else:
      if section['type'] == 'toc':
        r = chevron.render(toc_template, {"sections": toc})
        body += r
        body += "\n"

  config['body'] = body
  report_html = chevron.render(base_template, config)

  if args.debug:
    print(report_html)

  h = weasyprint.HTML(string=report_html, base_url='./', url_fetcher=fetcher)
  h.write_pdf("./" + '.pdf'.join(fname.rsplit('.toml', 1)))


if __name__ == "__main__":
  main()
