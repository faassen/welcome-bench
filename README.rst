Welcome Benchmark for Python Web Frameworks
===========================================

Usage
-----

This is a simple benchmark for Python web frameworks. To run them do
the following::

  $ virtualenv env
  $ source env/bin/activate
  $ pip install -r requirements.txt

You can then run the benchmarks::

  $ python benchmark.py

This prints out benchmark information for all the included frameworks.

If you want to ensure processor affinity you can try this::

  $ taskset python benchmark.py

You can repeat with environments for Python 2, Python 3 and PyPy.

To create a PyPy virtualenv::

  $ virtualenv --python=pypy env_pypy

To create a Python 3 virtualenv::

  $ virtualenv --python=python3 env_py3

``requirements.txt`` contains the latest release or release candidates
of the frameworks in question at the time of writing. It would be
interesting to have different sets of requirements so we can compare
changes over time.

What this means
----------------

The benchmark runs 100,000 requests against each web framework, using
the WSGI directly. No real HTTP server is therefore involved, nor are
any requests handled in parallel -- it only means how much time the
framework takes in Python.

``ms`` is the amount of milliseconds it took to fulfill all 100,000
requests. ``rps`` is the amount of requests per second the framework
was able to sustain.

The benchmark also runs a single request with the profiler after this,
and reports in ``tcalls`` how many function calls the request took,
and in ``funcs`` how many different functions were used to handle the
request.

Silly
-----

Be warned that this benchmark is silly in various ways:

* no real HTTP benchmarks are done, only WSGI stuff, single-threaded in
  a highly synthetic environment.

* Only "hello world" is benchmarked.

High performance in "hello world" is almost *never* useful in the real
world, as application code tends to dominate the framework by
far. Don't pick a framework because it has the highest numbers in this
benchmark. I realize it's tempting as it's such an easy thing to
bikeshed_ over, but don't.

.. _bikeshed: http://bikeshed.com/

Pick a framework because it's easy to use, because it's flexible,
because it helps you solve difficult problems. Only if you *know* you
are doing some low-level in-memory stuff where you need to have a
ridiculous throughput is where framework performance might start
becoming important.

To a web framework author like myself (Morepath_) a benchmark like
this is still useful as it gives an idea of how involved framework
code is, and to at least ensure it's not slower than some of the more
common web frameworks.

.. _Morepath: http://morepath.readthedocs.io

Options
-------

You use the ``-f`` flag to restrict the frameworks to benchmark, for
instance::

  $ python benchmark -f morepath -f flask

to benchmark just Flask and Morepath.

You can use the ``-n`` flag to change the number of requests to use
in the benchmark::

  $ python benchmark -n 1000

the default is 100000.

History
-------

This benchmark is adapted from the 01-hello example by Andriy
Kornatskyy, author of wheezy.web.

https://bitbucket.org/akorn/helloworld

I've simplified things considerably. I only install web frameworks
that seem to be reasonably popular and that are easy to install from
PyPI with pip. I've excluded some frameworks because they seemed very
slow; it's possible they aren't actually slow but that the benchmark
code was broken, but I didn't want to bother.

In addition there's Morepath_, authored by myself, and `wheezy.web`_,
as Andriy wrote that.

.. _Morepath: http://morepath.readthedocs.io

.. _wheezy.web: https://pythonhosted.org/wheezy.web/
