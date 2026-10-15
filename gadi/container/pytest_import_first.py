"""Import the installed UW3 package before pytest's collection-state guard."""
import sys
import underworld3
import pytest

raise SystemExit(pytest.main(sys.argv[1:]))
