from urllib.request import urlopen
from argparse import ArgumentParser
from hashlib import sha256
from datetime import datetime
import uuid
import os
import sys


class Client:
    def __init__(self, uri, title, cachedir=".cache", output_file="atom.xml"):
        """Args:
        uri: URI to read
        title: Title of the Atom feed
        cachedir: Path to this script's cache
        output_file: Atom feed to write to
        """
        self.uri = uri
        self.title = title
        self.cache = cachedir
        self.hashfile = os.path.join(self.cache, "hashes")
        self.feed_info = os.path.join(self.cache, "feed-info")
        self.tails = os.path.join(self.cache, "tails")
        self.output = output_file
        if not os.path.isdir(self.cache):
            os.mkdir(self.cache)
            with open(self.hashfile, "w") as hf:
                pass  # Create the file.
            with open(self.feed_info, "w") as fi:
                feed_id = str(uuid.uuid4())
                self.feed_id = feed_id
                fi.write(feed_id)
        else:
            with open(self.feed_info, "r") as fi:
                self.feed_id = fi.read()

    def read_page(self):
        """If the page is in the cache, return None. Otherwise, return
        its new text and add it to the cache."""

        rsp = urlopen(self.uri, timeout=10)
        text = rsp.read()
        hash = sha256(text).hexdigest()
        with open(self.hashfile, "r") as hf:
            if hash in hf.read():
                return None, hash
        with open(self.hashfile, "a") as hf:
            hf.write(hash + "\n")
        return text, hash

    def update_output(self):
        text, hash = self.read_page()
        if text is None:
            return
        with open(self.tails, "a") as tails:
            tails.write(
                f"""
<entry>\
  <title>{self.title} - {datetime.now().ctime()}</title>\
  <id>urn:btmh:{hash}</id>\
  <link href="{self.uri}" />\
</entry>
"""
            )
        with open(self.tails, "r") as entries:
            feed = entries.read()

        with open(self.output, "w") as of:
            of.write(
                f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<title>{self.title}</title>
<updated>{datetime.now().isoformat()}</updated>
<id>{self.feed_id}</id>
{feed}
</feed>
"""
            )


def parse_args(argv):
    parser = ArgumentParser(
        prog="Atomizer",
        description="""\
        Check a web site for updates, generate a new atom feed file if
        there are any.""",
    )
    parser.add_argument("uri", help="URI for thing to check")
    parser.add_argument("title", help="Title of the feed")
    parser.add_argument(
        "-o",
        "--outfile",
        default="atom.xml",
        help="Atom feed to update (default: atom.xml)",
    )
    parser.add_argument(
        "-c",
        "--cache-dir",
        default=".cache",
        help="Directory to use as cache (default: .cache)",
    )
    return parser.parse_args()


def run():
    print("Running...")
    args = parse_args(sys.argv[1:])
    c = Client(
        uri=args.uri,
        title=args.title,
        cachedir=args.cache_dir,
        output_file=args.outfile,
    )
    c.update_output()


if __name__ == "__main__":
    run()
