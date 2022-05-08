.. pypi-scan documentation master file, created by
   sphinx-quickstart on Sat Jun 27 06:15:52 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypi-scan's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Pypi-scan assists with your anti-typosquatting needs related to the python
package index (PyPI), a repository for open source Python programs.
Typosquatting refers to packages that use names similar to another, more
popular package to trick unsuspecting users into downloading malicious
software. PyPI, like many other package managers, has been been subject to
these typosquatting attacks in recent years; based on news reporting, there
have been at least several dozen documented typosquatting attacks on PyPI.

Pypi-scan can help detect typosquatting on PyPI. There are currently
four uses of pypi-scan:

- Scan PyPI for potential typosquatters on a particular package.
- Scan PyPI for potential typosquatters on the most downloaded
  packages.
- Scan packages recently added to PyPI for indications of typosquatting.
- Enumerate potential names that typosquatters might use to attack a
  particular package.

For further information on the threat of typosquatting, both in PyPI and
in other package repositories, and for possible defenses, see:

Nikolai Phillipp Tschacher, "Typosquatting in Programming Language Package
Managers," University of Hamburg, Bachelor Thesis, 2016.
Tschacher examines the extent to which users of PyPI and other package managers
are susceptible to typosquatting attacks. His conclusions? "Thousands of hosts
can be infected with malware by typosquatting package managers within a few
days."

Ruian Duan, Omar Alrawi, Ranjita Pai Kasturi, Ryan Elder, Brendan Saltaformaggio,
and Wenke Lee, "Measuring and Preventing Supply Chain Attacks on Package Managers,"
arXiv, 2020.
These researchers build an analytical pipeline, MalOSS, that finds over three
hundred malware on RubyGems (Ruby), NPM (nodeJS/Javascript), and PyPI. They
find seven instances of malware on PyPI.

Matthew Taylor, Ruturaj K. Vaidya, Drew Davidson, Lorenzo De Carli, and Vaibhav
Rastogi, "SpellBound: Defending Against Package Typosquatting," arXiv, 2020, available
at https://arxiv.org/pdf/2003.03471v1.pdf.
This is a system that helps a user importing libraries from PyPI or npm for
signs of typosquatting. Their approach combines typical lexical approaches with
a popularity score.

Marc Ohm, Henrik Plate, Arnold Sykosch, Michael Meier, "Backstabber's Knife Collection:
A Review of Open Source Software Supply Chain Attacks," arXiv, 2020,
https://arxiv.org/abs/2005.09535.
This paper presents a dataset of 174 malicious packages found on NPM,
PyPI, and RubyGems between 2015 and 2019.

Linux Foundation, "Open Source Software Supply Chain Security," February 2020.
This explicit "call to action" documents a number of high-profile software
supply chain attacks and then examines deficiencies in the current
software supply chain through the lens of developers, repositories, package
managers, and end users.

Matt Bullock, "pypi-parker," github, https://github.com/mattsb42, 2017.
Bullock wrote a piece of software that reduces the time needed for a package
manager to defensively register PyPI names a typosquatter might use.

ReversingLabs Research
This collection of blog posts examines the threat of malware in package
managers, especially npm and RubyGems.

https://blog.reversinglabs.com/blog/suppy-chain-malware-detecting-malware-in-package-manager-repositories
https://blog.reversinglabs.com/blog/the-npm-package-that-walked-away-with-all-your-passwords
https://blog.reversinglabs.com/newsroom/news/malicious-package-was-stealing-user-credentials-on-the-npm-repository
https://blog.reversinglabs.com/blog/mining-for-malicious-ruby-gems

More documentation coming soon!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
