# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 03/07/2023

### Fixed

- Fix previous broken build (did not include changes)

## [0.3.0] - 15/11/2021

### Fixed

- Fix parsing of empty dictionaries and `False` configuration values. These would
  previously be overridden by the downstream configuration.

## [0.2.0] - 28/09/2021

### Added

- Add none_overrides_value option. Before this change, None values would unexpectedly
  override previously configured values. Now, the previous value will be retained if
  newer values are None. The old behavior can be re-enabled with by setting the
  none_overrides_value argument of CascadeConfig to True.

## [0.1.0-a0] - 03/08/2020

### Added

- Initial release
