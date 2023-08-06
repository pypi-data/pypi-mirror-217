.. _SourceInstallation:

Contributors installation
-------------------------

Install from source
~~~~~~~~~~~~~~~~~~~

You can download the archive containing the sources from `CubicWeb
forge downloads section
<https://forge.extranet.logilab.fr/cubicweb/cubicweb/-/archive/branch/default/cubicweb-branch-default.zip>`_.

Make sure you also have all the :ref:`dependencies installed <InstallSourceDependencies>`.

Once uncompressed, you can install the framework from inside the uncompressed
folder with::

  pip install -e .

Or you can run |cubicweb| directly from the source directory by
setting the :ref:`resource mode <ResourcesConfiguration>` to `user`. This will
ease the development with the framework.

.. _MercurialInstallation:

Install from version control system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To keep-up with on-going development, clone the :ref:`Mercurial
<MercurialPresentation>` repository::

  hg clone -u 'last(tag())' https://forge.extranet.logilab.fr/cubicweb/cubicweb # stable version
  hg clone https://forge.extranet.logilab.fr/cubicweb/cubicweb # development branch

Make sure you also have all the :ref:`InstallSourceDependencies`.
