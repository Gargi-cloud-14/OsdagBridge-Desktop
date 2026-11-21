import pytest

from osdagbridge.core.bridge_types.plate_girder.bridge_geometry import (
    CrossSectionLayout,
    calculate_bridge_width,
)


def test_calculate_bridge_width_with_two_footpaths():
    """Check bridge width calculation for a bridge with two footpaths."""

    actual_width = calculate_bridge_width(
        carriageway_width=7.5,
        crash_barrier_width=0.5,
        median_width=1.0,
        no_of_footpaths=2,
        footpath_width=1.5,
        railing_width=0.2,
    )

    assert actual_width == pytest.approx(12.9)


def test_calculate_bridge_width_without_footpaths():
    """Check bridge width calculation when no footpaths are present."""

    actual_width = calculate_bridge_width(
        carriageway_width=7.5,
        crash_barrier_width=0.5,
        median_width=1.0,
        no_of_footpaths=0,
        footpath_width=1.5,
        railing_width=0.2,
    )

    assert actual_width == pytest.approx(9.5)


def test_cross_section_layout_total_width():
    """Check that the layout calculates the expected total bridge width."""

    layout = CrossSectionLayout(
        carriageway_width=7.5,
        crash_barrier_width=0.5,
        railing_width=0.2,
        footpath_width=1.5,
        median_width=1.0,
        no_of_footpaths=2,
    )

    assert layout.total_width == pytest.approx(12.9)


def test_cross_section_layout_component_positions():
    """Check the positions of important cross-section components."""

    layout = CrossSectionLayout(
        carriageway_width=7.5,
        crash_barrier_width=0.5,
        railing_width=0.2,
        footpath_width=1.5,
        median_width=1.0,
        no_of_footpaths=2,
    )

    components = {
        component.name: component
        for component in layout.components()
    }

    assert components["railing_left"].x_start == pytest.approx(0.0)
    assert components["railing_left"].x_end == pytest.approx(0.2)

    assert components["median"].x_start == pytest.approx(5.95)
    assert components["median"].x_end == pytest.approx(6.95)

    assert components["railing_right"].x_end == pytest.approx(12.9)


def test_cross_section_layout_accepts_matching_bridge_width():
    """A layout should accept a bridge with the same total width."""

    layout = CrossSectionLayout(
        carriageway_width=7.5,
        crash_barrier_width=0.5,
        railing_width=0.2,
        footpath_width=1.5,
        median_width=1.0,
        no_of_footpaths=2,
    )

    layout.validate_against_bridge(12.9)


def test_cross_section_layout_rejects_mismatched_bridge_width():
    """A layout should reject a bridge with a different total width."""

    layout = CrossSectionLayout(
        carriageway_width=7.5,
        crash_barrier_width=0.5,
        railing_width=0.2,
        footpath_width=1.5,
        median_width=1.0,
        no_of_footpaths=2,
    )

    with pytest.raises(ValueError):
        layout.validate_against_bridge(13.0)
