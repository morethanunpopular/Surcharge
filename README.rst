Surcharge
=========

**Surcharge** is a tool for benchmarking your web server like **apache benchmark**.

Surcharge uses the **gevent** networking library. Using the **greenlets** allow to spawn many concurrent requests with little memory.

HTTP requests are made with **requests** library.


Example
=======
::


  # simple call
  $ python surcharge.py --numbers 10 --concurrency 5 http://google.com

  Server: gws
  URL: http://google.com
  Concurrency level: 5
  Options: {}

  [----------]

  Number process requests: 10
  Time taken for tests: 5.91

  Complete requests: 10
  Failed requests: 0

  Faster request: 0.464
  Slower request: 5.443
  Time per request (only success): 1.226
  Request per second: 0.82

  # call with multiple cookies
  $ python surcharge.py http://httpbin.org/cookies --cookies ck:1, cook:value

  # call with HTTP Basic Auth
  $ python surcharge.py https://secure.test.com --auth user:password

  # bench during 10 seconds
  $ python surcharge.py http://google.com --concurrency 10 --duration 10

  # repeat the same bench twice
  $ python surcharge.py http://google.com --concurrency 10 --duration 10 --repeat 2

Install
=======
::


  $ pip install surcharge #and enjoy

Usage
=====
::


  usage: surcharge.py [-h] [-method {GET,POST,PUT,DELETE}]
                   [--concurrency CONCURRENCY] [--numbers NUMBERS]
                   [--cookies [COOKIES [COOKIES ...]]] [--content-type CT]
                   [--timeout TIMEOUT] [--auth AUTH] [--duration DURATION]
                   url

  Surcharge tools

  positional arguments:
    url                   URL you want overload

  optional arguments:
    -h, --help            show this help message and exit
    -method {GET,POST,PUT,DELETE}
                          HTTP method.
    --concurrency CONCURRENCY
                          Number of multiple requests to perform at a time.
                          Default is one request at a time.
    --numbers NUMBERS     Number of requests to perform for the benchmarking
                          session. Default is one request.
    --cookies [COOKIES [COOKIES ...]]
                          Send your own cookies. cookie:value
    --content-type CT     Specify our content-type.
    --timeout TIMEOUT     You can tell requests to stop waiting for a response
                          after a given number of seconds.
    --auth AUTH           Making requests with HTTP Basic Auth. user:password
    --duration DURATION   Duration. Override the --numbers option.
    --repeat REPEAT       Repeat the benchmark.
    --quiet               The general outcome is hidden.