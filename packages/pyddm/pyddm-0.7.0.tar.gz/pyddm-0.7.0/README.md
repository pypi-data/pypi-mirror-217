# PyDDM - Generalized drift-diffusion models for Python

# Overview

PyDDM is a simulator and modeling framework for generalized drift-diffusion
models (DDM), with a focus on cognitive neuroscience.

Key features include:

- Models solved numerically using Crank-Nicolson to solve the
  Fokker-Planck equation (Backward Euler, analytical solutions, and
  particle simulations also available)
- Arbitrary functions for drift rate, noise, bounds, and initial
  position distribution
- Arbitrary loss function and fitting method for parameter fitting
- Optional multiprocessor support
- Optional GUI for debugging and gaining an intuition for different
  models
- Convenient and extensible object oriented API allows building models
  in a component-wise fashion
- Verified accuracy of simulations using novel program verification
  techniques

See the [documentation](https://pyddm.readthedocs.io/en/latest/index.html),
[FAQs](https://pyddm.readthedocs.io/en/latest/faqs.html), or
[tutorial](https://pyddm.readthedocs.io/en/latest/quickstart.html) for more
information.  If you want to try it out before installing, visit the
[interactive online
demo](https://colab.research.google.com/github/mwshinn/PyDDM/blob/master/doc/notebooks/interactive_demo.ipynb).
See the [Github Forums](https://github.com/mwshinn/PyDDM/discussions) for help
from the PyDDM community.  You can also sign up for [release announcements by
email](https://www.freelists.org/list/pyddm-announce).


## Installation

Normally, you can install with:

    $ pip install pyddm

If you are in a shared environment (e.g. a cluster), install with:

    $ pip install pyddm --user

If installing from source, [download the source code](https://github.com/mwshinn/PyDDM), extract, and do:

    $ python3 setup.py install


## System requirements

- Python 3.5 or above
- Numpy version 1.9.2 or higher
- Scipy version 0.16.0 or higher
- Matplotlib
- [Paranoid Scientist](<https://github.com/mwshinn/paranoidscientist>)
- Pathos (optional, for multiprocessing support)
- A C compiler (If you don't already have one, the easiest way to install one
  may be by installing Cython.)


## Contact

For help on using PyDDM, see the [Github
Forums](https://github.com/mwshinn/PyDDM/discussions).

Please report bugs to <https://github.com/mwshinn/pyddm/issues>.  This
includes any problems with the documentation.  Pull Requests for bugs are
greatly appreciated.

Feature requests are currently not being accepted due to limited
resources.  If you implement a new feature in PyDDM, please do the
following before submitting a Pull Request on Github:

- Make sure your code is clean and well commented
- If appropriate, update the official documentation in the docs/
  directory
- Ensure there are Paranoid Scientist verification conditions to your
  code
- Write unit tests and optionally integration tests for your new
  feature (runtests.sh)
- Ensure all existing tests pass

For all other questions or comments, contact m.shinn@ucl.ac.uk.


## License

All code is available under the MIT license.  See LICENSE.txt for more
information.
