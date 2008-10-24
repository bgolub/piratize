import os
import pirate
import random
import urlparse
from BeautifulSoup import BeautifulSoup
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

def make_absolute(content, base):
    if not base.endswith('/'):
        base += '/'
    soup = BeautifulSoup(content)
    for a in soup.findAll('a'):
        try:
            if not a['href'].startswith('http://'):
                a['href'] = urlparse.urljoin(base, a['href'])
        except KeyError:
            pass
    for link in soup.findAll('link'):
        try:
            if not link['href'].startswith('http://'):
                link['href'] = urlparse.urljoin(base, link['href'])
        except KeyError:
            pass
    for script in soup.findAll('script'):
        try:
            if not script['src'].startswith('http://'):
                script['src'] = urlparse.urljoin(base, script['src'])
        except KeyError:
            pass
    for img in soup.findAll('img'):
        try:
            if not img['src'].startswith('http://'):
                img['src'] = urlparse.urljoin(base, img['src'])
        except KeyError:
            pass
    return soup


class MainPage(webapp.RequestHandler):
    def get(self):
        url = self.request.get('url', None)
        if not url:
            submit_values = (
                'Aarrr!',
                'Ahoy!',
                'Anchor\'s away!',
                'Avast matey!',
                'Fire the cannons!',
                'Load the cannons!',
                'Shiver me timbers!',
                'Walk the plank!',
            )
            template_values = {
                'submit_value': submit_values[random.randint(0, len(submit_values)-1)],
                'request': self.request,
            } 
            path = os.path.join(os.path.dirname(__file__), 'index.html')
            return self.response.out.write(template.render(path, template_values))
        if not url.startswith('http://'):
            url = 'http://' + url
        content = memcache.get(url)
        if not content:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                content = pirate.pirate(result.content)
            else:
                return self.error(result.status_code)
            content = make_absolute(content, url)
            memcache.set(url, content, 60*3)
        return self.response.out.write(content)
        

application = webapp.WSGIApplication([
    ('/', MainPage)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
