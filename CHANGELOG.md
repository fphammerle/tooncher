# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [1.0.1] - 2019-12-27
### Added
- package: use readme as long description for pypi.org

### Fixed
- `test_start_engine_mac` if `os.environ != {}`

## [1.0.0] - 2019-12-23
### Added
- path to tootown engine may be provided via env var `$TOONCHER_ENGINE_PATH`

### Changed
- command line interface:
  - fail if selected username was not found in config
  - fail if selected username has multiple entries in config
  - install via `setuptools.setup(entry_points=…)`
- python interface:
  - now private:
    - `tooncher.LOGIN_API_URL`
    - `tooncher.LoginDelayed`
    - `tooncher.LoginSuccessful`
    - `tooncher.TOONTOWN_ENGINE_DEFAULT_PATH`
    - `tooncher.api_request`
    - `tooncher.login`
  - `start_engine` & `launch`: expects `isinstance(engine_path, pathlib.Path)`
    (instead of `str`)
- pass all env vars to engine
  (e.g., enables use of `optirun tooncher …`)

### Removed
- python interface:
  - `argcomplete`
  - `tooncher.INVASIONS_API_URL`
  - `tooncher.InvasionProgress`
  - `tooncher.TOONTOWN_LIBRARY_PATH`
  - `tooncher.request_active_invasions`

### Fixed
- mac: `$DYLD_LIBRARY_PATH` & `$DYLD_FRAMEWORK_PATH` relative to engine path

## [0.4.1] - 2019-12-22
### Fixed
- `YAMLLoadWarning: […] the default Loader is unsafe. […]`

## [0.4.0] - 2017-10-31

[Unreleased]: https://github.com/fphammerle/tooncher/compare/1.0.1...HEAD
[1.0.1]: https://github.com/fphammerle/tooncher/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/fphammerle/tooncher/compare/0.4.1...1.0.0
[0.4.1]: https://github.com/fphammerle/tooncher/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/fphammerle/tooncher/compare/0.3.1...0.4.0
