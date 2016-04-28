from __future__ import print_function

import argparse
import os
import sys

PY3 = sys.version_info[0] >= 3
if PY3:
    from io import BytesIO
    ntob = lambda n, encoding: n.encode(encoding)
else:
    from cStringIO import StringIO as BytesIO
    ntob = lambda n, encoding: n

try:
    import cProfile as profile
except ImportError:
    import profile

from pstats import Stats
from timeit import timeit

known_frameworks = [
    'bottle',
    'django',
    'falcon',
    'flask',
    'morepath',
    'pyramid',
    'tornado',
    'wheezy.web',
    'wsgi',
]

environ = {
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;'
                   'q=0.9,*/*;q=0.8',
    'HTTP_ACCEPT_CHARSET': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'HTTP_ACCEPT_ENCODING': 'gzip,deflate,sdch',
    'HTTP_ACCEPT_LANGUAGE': 'uk,en-US;q=0.8,en;q=0.6',
    'HTTP_CACHE_CONTROL': 'max-age=0',
    'HTTP_CONNECTION': 'keep-alive',
    'HTTP_HOST': 'vm0.dev.local:8080',
    'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux i686)',
    'PATH_INFO': '/welcome',
    'QUERY_STRING': '',
    'REMOTE_ADDR': '127.0.0.1',
    'REQUEST_METHOD': 'GET',
    'REQUEST_URI': '/welcome',
    'SCRIPT_NAME': '',
    'SERVER_NAME': 'localhost',
    'SERVER_PORT': '8080',
    'SERVER_PROTOCOL': 'HTTP/1.1',
    'uwsgi.node': 'localhost',
    'uwsgi.version': '1.2.6',
    'wsgi.errors': None,
    'wsgi.file_wrapper': None,
    'wsgi.input': BytesIO(ntob('', 'utf-8')),
    'wsgi.multiprocess': False,
    'wsgi.multithread': False,
    'wsgi.run_once': False,
    'wsgi.url_scheme': 'http',
    'wsgi.version': (1, 0),
}


def start_response(status, headers, exc_info=None):
    return None


def run(frameworks, number):
    print("Benchmarking frameworks:", ', '.join(frameworks))
    sys.path[0] = '.'
    path = os.getcwd()
    print("                ms     rps  tcalls  funcs")
    for framework in frameworks:
        os.chdir(os.path.join(path, framework))
        try:
            main = __import__('app', None, None, ['main']).main

            f = lambda: list(main(environ.copy(), start_response))
            time = timeit(f, number=number)
            st = Stats(profile.Profile().runctx(
                'f()', globals(), locals()))
            print("%-11s %6.0f %7.0f %7d %6d" % (framework, 1000 * time,
                  number / time, st.total_calls, len(st.stats)))
            if 0:
                st = Stats(profile.Profile().runctx(
                    'timeit(f, number=number)', globals(), locals()))
                st.strip_dirs().sort_stats('time').print_stats(10)
            del sys.modules['app']
        except ImportError:
            print("%-15s not installed" % framework)


def main():
    parser = argparse.ArgumentParser("Benchmark Python web frameworks.")
    parser.add_argument('-f', '--framework', action='append',
                        choices=known_frameworks)
    parser.add_argument('-n', '--number', type=int, default=100000)

    args = parser.parse_args()
    frameworks = args.framework
    if not frameworks:
        frameworks = sorted(known_frameworks)
    run(frameworks, args.number)


if __name__ == '__main__':
    main()
