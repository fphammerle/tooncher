# tooncher
automates toontown rewritten's login process

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation

```sh
$ pip3 install --user --upgrade tooncher
```

Optional: Install cpulimit to enable use of parameter `--cpu-limit`

```sh
$ sudo apt-get install cpulimit
```

## Configuration

```yaml
# default path: $HOME/.tooncher
accounts:
- username: toon
  password: secret
- username: ceo
  password: golf
- username: cfo
  password: train
engine_path: '/opt/Toontown Rewritten/TTREngine'
```

## Usage

```sh
$ tooncher [username]
```

`tooncher --help` shows all available options.

### Examples

```sh
$ tooncher toon
$ tooncher ceo
$ tooncher --cpu-limit 70 cfo
```
