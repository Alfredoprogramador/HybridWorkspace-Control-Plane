"""Pytest configuration."""
import pytest


@pytest.fixture(autouse=True)
def reset_event_loop_policy():
    """Use asyncio event loop for all async tests."""
    pass
