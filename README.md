# BEEhaviourLab

[![tests](https://github.com/BEEhaviourLab/BEEhaviourLab/actions/workflows/tests.yml/badge.svg)](https://github.com/BEEhaviourLab/BEEhaviourLab/actions/workflows/tests.yml)

BEEhaviourLab provides tools for detecting, tracking, and analysing bee behaviour from video data. Tracking data is output to CSV files for downstream analyses. The object detection (YOLO) model can be substituted for your own to enable different use-cases. 

## Documentation
-------------
Full documentation is published on GitHub Pages:
https://beehaviourlab.github.io/BEEhaviourLab/

## Installation
------------
Install from PyPI:

```
pip install beehaviourlab
```

For more other installation options, please see the [installation docs](https://beehaviourlab.github.io/BEEhaviourLab/installation.html).

## Configuration and command line use

For more comprehensive instructions, please see the [docs pages](https://beehaviourlab.github.io/BEEhaviourLab/).

### Tracking module
---------------

#### Configuration
-------------
To create editable config files in your working directory:

```
bee config init
```

This writes:
- `tracking_config.yaml`
- `tracking/custom_tracker.yaml`

The CLI will automatically use a `tracking_config.yaml` in your current working
directory if present.

All tracking commands are available under the `bee track` group.

#### Common commands:

Run the entire bee tracking pipeline on a video file:

```
bee track run-pipeline --input /path/to/video_file --output /path/to/output_dir
```

#### Batch processing
----------------
There is a batch-processing command for running the tracking pipeline over all videos in a
directory tree and writing outputs into a per-video subdirectory.

Usage:

`bee track batch-process --input-dir /path/to/videos`

You can also filter the video files to just those that contain a particular string, in this example "hiveA":

`bee track batch-process --input-dir /path/to/videos --filter hiveA`

## Contributing

We welcome contributions from the community. Please take a look at our [contribution guidelines](https://github.com/BEEhaviourLab/BEEhaviourLab?tab=contributing-ov-file) for more information.
