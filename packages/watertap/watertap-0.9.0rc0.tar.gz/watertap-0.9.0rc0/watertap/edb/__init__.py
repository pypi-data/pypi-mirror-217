#################################################################################
# WaterTAP Copyright (c) 2020-2023, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory, Oak Ridge National Laboratory,
# National Renewable Energy Laboratory, and National Energy Technology
# Laboratory (subject to receipt of any required approvals from the U.S. Dept.
# of Energy). All rights reserved.
#
# Please see the files COPYRIGHT.md and LICENSE.md for full copyright and license
# information, respectively. These files are also available online at the URL
# "https://github.com/watertap-org/watertap/"
#################################################################################
"""
Electrolyte database.

Design::

     ┌────────────────────────────┐
     │           Validate         │
     │  ┌───────┐    ┌──────┐     │
     │  │JSON   │    │JSON  │     │
     │  │input  │    │schema│     │
     │  │data   │    │      │     │
     │  └───────┴┐ ┌─┴──────┘     │
     │           │ │              │
     │        ┌──▼─▼───┐          │
     │        │        │NO        │
     │        │ VALID? ├───►Error │
     │        └────┬───┘          │
     │             │              │
     │             │YES           │
     └─────────────┼──────────────┘
                   │                      ┌───────────────┐
     DB API........│.....                 │  reaction     │
        ...    ┌───▼───┐ ..    ;;;;;;;;   ├───────────────┤
       ..      │Load   ├──.───►;      ;   │  component    │
      ..       └───────┘  .    ; DB   ;───┼───────────────┤
     .          ▲         ..   ;      ;   │  base         │
    ..          │          .   ;;;;;;;;   ├───────────────┤
    .           │           ...           └───────────────┘
    .           │              ...        ...........................
    .   ┌───────▼┐    ┌─────────┐...    ...──────────┐   ┌───────────...
    .   │ Search ├───►│ Fetch   │  .   .. │ Component◄──o│ HasConfig │ .
    ..  └────────┘    └────┬────┘  .  ..  └──────▲───┘   └───o───────┘  .
     ...                   │      .  ..          │           │          .
        ...                │    ...  .           │           │         ..
           .....           │  ...   ..   ┌───────x───┐       │         .
                 . ... .. .│...     .    │ Reaction  │◄──────┘        ..
                           │        .    └─────▲─────┘                .
                           │        .          │                    ..
                           │        .  **┌─────x───┐               ..
                           └─────────.──►│ Result  │     Data model
                                     ... └─────────┘            ..
                                       .....                ....
                                            ............ ...
"""
__author__ = "Dan Gunter"

# Convenience imports
from .db_api import ElectrolyteDB
