#!/usr/bin/env python
"""Tests for `lolcatt` package."""
import lolcatt


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    print(lolcatt.__version__)
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
