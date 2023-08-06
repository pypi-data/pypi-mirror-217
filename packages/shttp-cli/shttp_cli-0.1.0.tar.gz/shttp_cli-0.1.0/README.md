# An extremely tiny and straightforward HTTP client

## Installation

shttp is a Python script. You may install it using [pip](https://pip.pypa.io/en/stable/):

```sh
pip install shttp-cli
```

## Basic usage

### Send a GET request

```sh
shttp http://httpbin.org/get
```

### Send a POST request

```sh
shttp --method POST http://httpbin.org/post
```

or

```sh
shttp -m POST http://httpbin.org/post
```

### Send a POST request with a body

```sh
shttp -m POST http://httpbin.org/post -d '{"foo": "bar"}'
```

## Licensing

This code is released under the [GPLv3 license](./LICENSE).
