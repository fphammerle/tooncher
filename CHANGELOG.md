# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Changed
- install command line interface via `setuptools.setup(entry_points=…)`
- now private:
  - `tooncher.LOGIN_API_URL`
  - `tooncher.LoginDelayed`
  - `tooncher.LoginSuccessful`
  - `tooncher.api_request`

### Removed
- `argcomplete`
- `tooncher.INVASIONS_API_URL`
- `tooncher.InvasionProgress`
- `tooncher.request_active_invasions`

## [0.4.1] - 2019-12-22
### Fixed
- `YAMLLoadWarning: […] the default Loader is unsafe. […]`

## [0.4.0] - 2017-10-31

[Unreleased]: https://github.com/fphammerle/tooncher/compare/0.4.1...HEAD
[0.4.1]: https://github.com/fphammerle/tooncher/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/fphammerle/tooncher/compare/0.3.1...0.4.0
