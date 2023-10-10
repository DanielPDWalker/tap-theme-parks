# tap-theme-parks

[![test](https://github.com/DanielPDWalker/tap-theme-parks/actions/workflows/test.yml/badge.svg)](https://github.com/DanielPDWalker/tap-theme-parks/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<a href="https://github.com/DanielPDWalker/tap-theme-parks/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/DanielPDWalker/tap-theme-parks"></a>
[![Python](https://img.shields.io/static/v1?logo=python&label=python&message=3.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11&color=blue)]()

`tap-theme-parks` is a Singer tap for theme park data from [themeparks.wiki](https://themeparks.wiki/) API, built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.


## Installation

Add directly to your Meltano project from the Meltano Hub:

```bash
meltano add extractor tap-theme-parks
```

Or install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-themeparks.git@main
```


## Configuration

There are no required settings for `tap-theme-parks`, only optional settings to get specific data.

### Settings

Setting | Required | Type | Description | Environment Variable |
------- | -------- | ---- | ----------- | -------------------- |
`live_data_array` | Optional | Array of String | An array of id or slugs (can be found from the `destinations` data) that you want to get live data for. This can include queue times, show times and operating hours. | `TAP_THEME_PARKS_LIVE_DATA_ARRAY`

**Note that you enable the live data streams by supplying this setting.**

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-themeparks --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Usage

You can easily run `tap-themeparks` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-themeparks --version
tap-themeparks --help
tap-themeparks --config CONFIG --discover > ./catalog.json
```

---

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-themeparks` CLI interface directly using `poetry run`:

```bash
poetry run tap-themeparks --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-themeparks
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-themeparks --version
# OR run a test `elt` pipeline:
meltano elt tap-themeparks target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
