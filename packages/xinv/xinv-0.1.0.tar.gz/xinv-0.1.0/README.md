# xinv

A CLI tool for generating customized invoices. The content is hardcoded in
a configuration file but can be overridden with command options.

Created specifically for personal needs, so probably not suitable for others.
The tool officially supports and is distributed only for macOS. Very likely,
it works also on other Unix-like systems but no quality checks are done
for them.

## Usage

```sh
$ xinv
Usage: xinv [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create
  init
```

## Contributing

### Running Tests

Besides Python packages required for testing, extra tools have to be installed
in your system in order to successfully run regression tests.
Please follow the instructions below.

### macOS

```sh
brew install wkhtmltopdf imagemagick poppler
```
