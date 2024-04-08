from .patterns import (
    bms_patterns,
    chakravorty_patterns,
    dundee_patterns,
    glaxo_patterns,
    lint_patterns,
    mlsmr_patterns,
    pains_patterns,
    sure_chembl_patterns,
)

__all__ = ["hitdexter_patterns"]

"""
Description: Filter sets that are used in the Hit Dexter 2.0 web service. 
For details see: https://pubs.acs.org/doi/pdf/10.1021/acs.jcim.8b00677
"""
hitdexter_patterns = {
    "pains": pains_patterns,
    "bms": bms_patterns,
    "dundee": dundee_patterns,
    "glaxo": glaxo_patterns,
    "lint": lint_patterns,
    "mlsmr": mlsmr_patterns,
    "sure_chembl": sure_chembl_patterns,
    "chakravorty": chakravorty_patterns,
}
