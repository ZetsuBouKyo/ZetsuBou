# Welcome to ZetsuBou

[![Python](https://img.shields.io/badge/Python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-3811/)
[![Vue](https://img.shields.io/badge/Vue-3.3.4-yellow.svg)](https://v3.vuejs.org/)
[![chrome](https://img.shields.io/badge/Chrome-115.0.5790.99-yellow.svg)](https://www.google.com/intl/en_us/chrome/)
[![license](https://img.shields.io/badge/License-MIT-yellow.svg)](https://www.google.com/intl/en_us/chrome/)

This is a self-hosted web application for your own image galleries and videos on the
Linux operating system.

??? warning "Currently we only support the Linux operating system"

    **Other operating** systems are not supported due to time constraints.

??? warning "We will generate folders `.tag` in your galleries"

    ZetsuBou would generate `.tag` folders inside your galleries. Here is an example of
    the folder structure.

    ```text
    <your image galleries>
    ├── <your image gallery 001>
    │   ├── 1.jpg
    │   ├── 2.jpg
    │   ├── 3.jpg
    │   ├── 4.jpg
    │   ├── 5.jpg
    │   └── .tag
    │       └── gallery.json
    └── <your image gallery 002>
        ├── 1.jpg
        ├── 2.jpg
        ├── 3.jpg
        ├── 4.jpg
        └── .tag
            └── gallery.json
    ```

![Alt Text](assets/example/preview-galleries.png)
