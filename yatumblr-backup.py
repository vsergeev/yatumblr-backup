#!/usr/bin/env python
#
# yet another tumblr backup script - vsergeev
# Downloads blog info and all raw posts and writes them to a file in JSON.
#

import sys
import time
import json

if sys.version > "3":
    from urllib.request import urlopen
else:
    from urllib import urlopen

################################################################################

try:
    TUMBLR_API_KEY = open("apikey").read().strip()
except:
    sys.stderr.write("Please place Tumblr API key in file 'apikey'!\n")
    sys.exit(1)

################################################################################

class TumblrAPIException(Exception): pass

def tumblr_api_get(url):
    try:
        f = urlopen(url)
        response = json.loads(f.read().decode('utf-8'))
        f.close()
    except Exception as e:
        raise TumblrAPIException("error with API get: %s" % str(e))

    try:
        if response['meta']['status'] != 200:
            raise TumblrAPIException("invalid response code: %d" % response['meta']['status'])
    except KeyError:
        raise TumblrAPIException("invalid response")

    return response['response']

def tumblr_blog_info(blog):
    url = "http://api.tumblr.com/v2/blog/{0}/info?api_key={1}".format(blog, TUMBLR_API_KEY)
    return tumblr_api_get(url)['blog']

def tumblr_posts_info(blog, offset, num=20):
    url = "http://api.tumblr.com/v2/blog/{0}/posts?api_key={1}&offset={2}&limit={3}&reblog_info=true&notes_info=true&filter=raw".format(blog, TUMBLR_API_KEY, offset, num)
    return tumblr_api_get(url)['posts']

################################################################################

if len(sys.argv) < 2:
    sys.stderr.write("Usage: %s <tumblr hostname> [target directory]\n" % sys.argv[0])
    sys.stderr.write("e.g.   %s myblog.tumblr.com\n" % sys.argv[0])
    sys.exit(1)

blog = sys.argv[1]
directory = "./" if len(sys.argv) < 3 else sys.argv[2]
if directory[-1] != "/":
    directory += "/"

backup = {}
backup['blog_info'] = tumblr_blog_info(blog)
backup['blog_posts'] = []

print("Total number of posts: %d" % backup['blog_info']['posts'])

while len(backup['blog_posts']) < backup['blog_info']['posts']:
    offset = len(backup['blog_posts'])
    backup['blog_posts'] += tumblr_posts_info(blog, offset)
    sys.stdout.write("\rTotal posts fetched:   %d" % len(backup['blog_posts']))

print("\n\nDone!")

timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
filename = "backup-{0}-{1}.json".format(blog, timestr)

with open(directory + filename, "w") as f:
    f.write(json.dumps(backup, indent=4, sort_keys=True))

print("Backup written to %s" % (directory + filename))

