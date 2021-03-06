## yet another tumblr backup script

yatumblr-backup (yet another tumblr backup script) fetches blog info and all raw posts and writes them to a gzipped JSON file. The fetched content is retained in the original JSON format returned by the [Tumblr API](http://www.tumblr.com/docs/en/api). If tumblr gets nuked you can post-process the high fidelity JSON later.

Requires a [Tumblr API key](http://www.tumblr.com/oauth/apps) stored in file `apikey`. Compatible with both Python 2 and Python 3.

```
Usage: yatumblr-backup.py <tumblr hostname> [target directory]
e.g.   yatumblr-backup.py myblog.tumblr.com
e.g.   yatumblr-backup.py myblog.tumblr.com /path/to/backups
```

```
$ ./yatumblr-backup.py myblog.tumblr.com
Total number of posts: 263
Total posts fetched:   263

Done!
Backup written to ./backup-myblog.tumblr.com-2013-10-12-16-02-17.json.gz
$
```

### Notes

  * yatumblr-backup does not fetch images used in text or image posts.
  * yatumblr-backup does not fetch blog static pages or stylesheets.

