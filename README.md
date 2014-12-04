MMEDIARHEL7
===========

RPM spec files for FFmpeg and related multimedia libraries for RHEL / CentOS 7

Binary (and src) RPMs for x86_64 are available at
http://awel.domblogger.net/7/media/

If you are interested in FFmpeg or the other multi-media packages for RHEL /
CentOS 7 I suggest you use the yum repository available at that link rather
than using these spec files to build them yourself, but of course you can use
these spec files to build them yourself if you would prefer.

About
-----

The packages in the AWEL media repository exist to provide ffmpeg 2.4.x support
for CentOS / RHEL 7. Additional packages were added to provide support for a
modern and more complete GStreamer environment. The more modern GStreamer
itself however is in a separate package repository.

Finally a few misc. multimedia packages that were missing from CentOS / EPEL
were added (e.g. python-eyeD3)

Most of the RPM spec files come from Fedora 18, 19, 20 and RPMFusion for
CentOS / RHEL 7. A few I wrote.

Patches are in the `patches` sub-directory. Most of them were not written by
me, but some were (e.g. the `eyeD3-lameinfo.patch` patch)

The purpose of this git is to provide a place where the RPM spec files and/or
patches can be obtained without needing to download the `src.rpm` files.

This is also the best replace to report any problems with the packages that you
may encounter.

Enjoy.
