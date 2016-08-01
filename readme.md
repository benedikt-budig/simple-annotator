Simple Annotator
================
This is a simple tool for annotating images with lines of text. It is useful for
creating ground truth (aka "gold standards"), which can for instance be used to
train OCR engines like [ocropy](https://github.com/tmbdev/ocropy).

Usage
-----
Simple Annotator presents image from a given directory, one at a time, and lets
the user annotate each image with a line of text. The annotation is saved as
plain text to the same directory.

To annotate the images in the `example` directory, type:

    ./simple-annotator.py example/

License
-------
Simple Annotator is free software and licensed under the GNU General Public License version 3.
