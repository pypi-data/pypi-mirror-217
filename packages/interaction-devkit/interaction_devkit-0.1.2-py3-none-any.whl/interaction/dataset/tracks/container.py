"""Track data containers for the INTERACTION dataset.

This module provides the following containers:

- :class:`MotionState`: A single motion state of an agent at a time step.
- :class:`Track`: A single track.
- :class:`INTERACTIONCase`: A single case of observation in a scenario.
"""
# Copyright (c) 2023, Juanwu Lu <juanwu@purdue.edu>.
# Released under the BSD-3-Clause license.
# See https://opensource.org/license/bsd-3-clause/ for licensing details.
import math
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from functools import cached_property
from itertools import chain
from typing import Any, Optional, Union

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.affinity import rotate, translate
from shapely.geometry import LineString, Point, Polygon

from ..utils import LOCATIONS
from .typing import AgentType

# Constants
MOTION_STATE_FIELD_MAPPING = {
    "timestamp_ms": "timestamp_ms",
    "x": "position_x",
    "y": "position_y",
    "vx": "velocity_x",
    "vy": "velocity_y",
    "psi_rad": "heading",
    "length": "length",
    "width": "width",
}


@dataclass(frozen=True)
class MotionState:
    """A single motion state of an agent at a time step."""

    agent_id: int
    """int: The ID of the agent in a case."""
    timestamp_ms: int
    """int: The timestamp of the motion state in milliseconds."""
    position_x: float
    """float: The x-coordinate of the position of the agent in meters."""
    position_y: float
    """float: The y-coordinate of the position of the agent in meters."""
    velocity_x: float
    """float: The x-component of the velocity in meters per second."""
    velocity_y: float
    """float: The y-component of the velocity in meters per second."""
    heading: Optional[float] = None
    """float: The heading of the agent in radians."""
    length: Optional[float] = None
    """float: The length of the agent in meters."""
    width: Optional[float] = None
    """width: The width of the agent in meters."""

    def __post_init__(self) -> None:
        """Post-initialization hook."""
        assert (
            isinstance(self.agent_id, int) and self.agent_id >= 0
        ), f"Agent ID must be a non-negative int, but got {self.agent_id}"
        assert (
            isinstance(self.timestamp_ms, int) and self.timestamp_ms >= 100
        ), f"Timestamp must be a non-negative int, but got {self.timestamp_ms}"
        assert isinstance(self.position_x, float), "Position x must be a float"
        assert isinstance(self.position_y, float), "Position y must be a float"
        assert isinstance(self.velocity_x, float), "Velocity x must be a float"
        assert isinstance(self.velocity_y, float), "Velocity y must be a float"
        assert isinstance(
            self.heading, (float, type(None))
        ), "Heading must be a float or None"
        assert isinstance(
            self.length, (float, type(None))
        ), "Length must be a float or None"
        assert isinstance(
            self.width, (float, type(None))
        ), "Width must be a float or None"

    @cached_property
    def bounding_box(self) -> Polygon:
        """Optional[Polygon]: The bounding box of the current motion state."""
        if (
            self.heading is None
            or math.isnan(self.heading)
            or self.length is None
            or math.isnan(self.length)
            or self.width is None
            or math.isnan(self.width)
        ):
            return Point(self.position_x, self.position_y).buffer(0.75)

        half_length = self.length / 2.0
        half_width = self.width / 2.0

        # corners in the local coordinate system
        bounding_box = Polygon(
            [
                # rear-right corner
                Point(-half_length, -half_width),
                # rear-left corner
                Point(-half_length, half_width),
                # front-left corner
                Point(half_length, half_width),
                # front-right corner
                Point(half_length, -half_width),
            ]
        )
        # affine transform
        bounding_box = translate(
            geom=rotate(
                geom=bounding_box, angle=self.heading, use_radians=True
            ),
            xoff=self.position_x,
            yoff=self.position_y,
        )

        return bounding_box

    @property
    def speed(self) -> float:
        """float: The speed of the agent in meters per second."""
        return math.hypot(self.velocity_x, self.velocity_y)

    def to_geometry(self) -> Point:
        """Convert the motion state to a Shapely geometry object.

        Returns:
            Point: The motion state as a Shapely geometry object.
        """
        return Point(self.position_x, self.position_y)

    def __eq__(self, __value: Any) -> bool:
        if isinstance(__value, MotionState):
            return hash(self) == hash(__value)
        return NotImplemented

    def __ne__(self, __value: Any) -> bool:
        if isinstance(__value, MotionState):
            return hash(self) != hash(__value)
        return NotImplemented

    def __ge__(self, __value: Any) -> bool:
        if (
            isinstance(__value, MotionState)
            and self.agent_id == __value.agent_id
        ):
            return self.timestamp_ms >= __value.timestamp_ms
        return NotImplemented

    def __gt__(self, __value: Any) -> bool:
        if (
            isinstance(__value, MotionState)
            and self.agent_id == __value.agent_id
        ):
            return self.timestamp_ms > __value.timestamp_ms
        return NotImplemented

    def __le__(self, __value: Any) -> bool:
        if (
            isinstance(__value, MotionState)
            and self.agent_id == __value.agent_id
        ):
            return self.timestamp_ms <= __value.timestamp_ms
        return NotImplemented

    def __lt__(self, __value: Any) -> bool:
        if (
            isinstance(__value, MotionState)
            and self.agent_id == __value.agent_id
        ):
            return self.timestamp_ms < __value.timestamp_ms
        return NotImplemented

    def __hash__(self) -> int:
        return hash(
            (
                self.agent_id,
                self.timestamp_ms,
                self.position_x,
                self.position_y,
                self.velocity_x,
                self.velocity_y,
                self.heading,
                self.length,
                self.width,
            )
        )

    def __str__(self) -> str:
        attr_str = ", ".join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"<{self.__class__.__name__}({attr_str}) at {hex(id(self))}>"

    def __repr__(self) -> str:
        return str(self)


@dataclass(frozen=True)
class Track:
    """A single track consisting of motion states of the same agent."""

    agent_id: int
    """int: The ID of the agent in a case."""
    type: AgentType
    """AgentType: The type of the agent."""
    motion_states: tuple[MotionState, ...] = ()
    """Tuple[MotionState, ...]: The motion states of the agent."""

    def __post_init__(self) -> None:
        """Post-initialization hook."""
        assert (
            isinstance(self.agent_id, int) and self.agent_id >= 0
        ), "Agent ID must be a non-negative int"
        assert isinstance(
            self.type, AgentType
        ), "Agent type must be an `AgentType` object."
        assert isinstance(self.motion_states, Iterable) and all(
            isinstance(ms, MotionState) and ms.agent_id == self.agent_id
            for ms in self.motion_states
        ), "Motion states must be an iterable of `MotionState` objects with the same agent ID."

        # sort the motion states by timestamp
        object.__setattr__(
            self, "motion_states", tuple(sorted(self.motion_states))
        )

    @cached_property
    def bounding_boxes(self) -> list[Polygon]:
        """List[Polygon]: The bounding boxes of the track."""
        return [ms.bounding_box for ms in self.motion_states]

    @cached_property
    def timestamps(self) -> list[int]:
        """List[int]: The timestamps of the track in milliseconds."""
        return [ms.timestamp_ms for ms in self.motion_states]

    @cached_property
    def min_timestamp_ms(self) -> float:
        """float: The minimum timestamp of the track in milliseconds."""
        return min(ms.timestamp_ms for ms in self.motion_states)

    @cached_property
    def max_timestamp_ms(self) -> float:
        """float: The maximum timestamp of the track in milliseconds."""
        return max(ms.timestamp_ms for ms in self.motion_states)

    @property
    def num_motion_states(self) -> int:
        """int: The number of motion states in the track."""
        return len(self.motion_states)

    def to_geometry(self) -> LineString:
        """Convert the track to a Shapely geometry object.

        Returns:
            LineString: The track as a Shapely geometry object.
        """
        return LineString(
            [(ms.position_x, ms.position_y) for ms in self.motion_states]
        )

    def __eq__(self, __value: Any) -> bool:
        if isinstance(__value, Track):
            return hash(self) == hash(__value)
        return NotImplemented

    def __ne__(self, __value: Any) -> bool:
        if isinstance(__value, Track):
            return hash(self) != hash(__value)
        return NotImplemented

    def __ge__(self, __value: Any) -> bool:
        if isinstance(__value, Track):
            return self.agent_id >= __value.agent_id
        return NotImplemented

    def __gt__(self, __value: Any) -> bool:
        if isinstance(__value, Track):
            return self.agent_id > __value.agent_id
        return NotImplemented

    def __le__(self, __value: Any) -> bool:
        if isinstance(__value, Track):
            return self.agent_id <= __value.agent_id
        return NotImplemented

    def __lt__(self, __value: Any) -> bool:
        if isinstance(__value, Track):
            return self.agent_id < __value.agent_id
        return NotImplemented

    def __getitem__(self, __index: int) -> MotionState:
        """Get the motion state at the given index."""
        return self.motion_states[__index]

    def __iter__(self) -> Iterator[MotionState]:
        """Return an iterator over the motion states of the track."""
        return iter(self.motion_states)

    def __len__(self) -> int:
        """Get the number of motion states in the track."""
        return len(self.motion_states)

    def __hash__(self) -> int:
        return hash((self.agent_id, self.type, self.motion_states))

    def __str__(self) -> str:
        attr_str = ", ".join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"<{self.__class__.__name__}({attr_str}) at {hex(id(self))}>"

    def __repr__(self) -> str:
        return str(self)


@dataclass
class INTERACTIONCase:
    """A single case of observation in a scenario."""

    location: str
    """str: The location name of the case."""
    case_id: int
    """int: The ID of the case."""
    history_tracks: tuple[Track] = ()
    """Tuple[Track, ...]: The history tracks of the case."""
    current_tracks: tuple[Track] = ()
    """Tuple[Track, ...]: The current tracks of the case."""
    futural_tracks: tuple[Track] = ()
    """Tuple[Track, ...]: The futural tracks of the case."""
    tracks_to_predict: tuple[int] = ()
    """Tuple[int, ...]: The IDs of the tracks to predict."""
    interesting_agents: tuple[int] = ()
    """Tuple[int, ...]: The IDs of the interesting agents (ego vehicles)."""

    def __post_init__(self) -> None:
        """Post-initialization hook."""
        assert self.location in LOCATIONS, "Invalid location name"
        assert (
            isinstance(self.case_id, int) and self.case_id >= 0
        ), "Expected a non-negative integer for case ID."

        self.history_tracks = sorted(self.history_tracks)
        self._history_ids = (track.agent_id for track in self.history_tracks)
        self.current_tracks = sorted(self.current_tracks)
        self._current_ids = (track.agent_id for track in self.current_tracks)
        self.futural_tracks = sorted(self.futural_tracks)
        self._futural_ids = (track.agent_id for track in self.futural_tracks)
        self.tracks_to_predict = tuple(self.tracks_to_predict)
        self.interesting_agents = tuple(self.interesting_agents)

    @cached_property
    def num_agents(self) -> int:
        """int: The number of agents in the case."""
        return len(
            {
                track.agent_id
                for track in chain(
                    self.history_tracks,
                    self.current_tracks,
                    self.futural_tracks,
                )
            }
        )

    def get_history_track(self, agent_id: int) -> Optional[Track]:
        if agent_id not in self._history_ids:
            return None
        _index = self._history_ids.index(agent_id)
        return self.history_tracks[_index]

    def get_history_tracks(self) -> Iterator[Track]:
        yield from self.history_tracks

    def get_current_motion_state(self, agent_id: int) -> Optional[MotionState]:
        if agent_id not in self._current_ids:
            return None
        _index = self._current_ids.index(agent_id)
        return self.current_tracks[_index][-1]

    def get_current_motion_states(self) -> Iterator[MotionState]:
        for track in self.current_tracks:
            yield track[-1]

    def get_futural_track(self, agent_id: int) -> Optional[Track]:
        if agent_id not in self._futural_ids:
            return None
        _index = self._futural_ids.index(agent_id)
        return self.futural_tracks[_index]

    def get_futural_tracks(self) -> Iterator[Track]:
        yield from self.futural_tracks

    def render(
        self,
        anchor: Optional[tuple[float, float, float]] = None,
        ax: Optional[plt.Axes] = None,
        mode: str = "tail-box",
    ) -> Union[plt.Axes, list[plt.Axes]]:
        """Render the case.

        Args:
            anchor (Optional[Tuple[float, float, float]]): The anchor point of
            the case, and if it is `None`, the case will be rendered at the
            original positions. Defaults to `None`.
            ax (Optional[plt.Axes]): The axes to render the case, and if it is
            `None`, a new figure will be created. Defaults to `None`.
            mode (str): The mode to render the case, and it must be one of
            `["tail-box", "full-line", "full-box", "animation"]`. Defaults to
            `"tail-box"`.

        Returns:
            plt.Axes: The axes to render the case.
        """
        assert mode in [
            "tail-box",
            "full-line",
            "full-box",
            "animation",
        ], "Invalid mode."
        if ax is None:
            _, ax = plt.subplots(figsize=(10, 10))

        if anchor is not None:
            assert (
                len(anchor) == 3
            ), "Invalid anchor point: must be a 2D pose with [x, y, heading]."
            x, y, heading = anchor
            cosine, sine = math.cos(heading), math.sin(heading)
            xoff, yoff = -x * cosine + y * sine, -x * sine - y * cosine
            affine_params = [cosine, -sine, sine, cosine, xoff, yoff]
        else:
            affine_params = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

        # plot the history tracks
        if mode in ["tail-box", "full-line"]:
            # render the history and future tracks as lines, and the current
            # motion states as boxes
            gpd.GeoSeries(
                [
                    track.to_geometry()
                    for track in self.history_tracks
                    if track.agent_id not in self.tracks_to_predict
                ]
            ).affine_transform(affine_params).plot(
                ax=ax, color="#00CFFD", linewidth=1, zorder=12
            )
            gpd.GeoSeries(
                [
                    track.to_geometry()
                    for track in self.history_tracks
                    if track.agent_id in self.tracks_to_predict
                ]
            ).affine_transform(affine_params).plot(
                ax=ax, color="#F29492", linewidth=1, zorder=12
            )
            gpd.GeoSeries(
                [track.to_geometry() for track in self.futural_tracks]
            ).affine_transform(affine_params).plot(
                ax=ax, color="#A8FF78", linewidth=1, zorder=13
            )
            if mode == "tail-box":
                gpd.GeoSeries(
                    [
                        motion_state.bounding_box
                        for motion_state in self.get_current_motion_states()
                        if motion_state.agent_id not in self.tracks_to_predict
                    ]
                ).affine_transform(affine_params).plot(
                    ax=ax,
                    ec="#000000",
                    fc="#00CFFD",
                    lw=1.0,
                    alpha=0.6,
                    zorder=11,
                )
                gpd.GeoSeries(
                    [
                        motion_state.bounding_box
                        for motion_state in self.get_current_motion_states()
                        if motion_state.agent_id in self.tracks_to_predict
                    ]
                ).affine_transform(affine_params).plot(
                    ax=ax,
                    ec="#000000",
                    fc="#F29492",
                    lw=1.0,
                    alpha=0.6,
                    zorder=11,
                )
            return ax
        elif mode == "full-box":
            # TODO: render the full tracks as boxes
            raise NotImplementedError
        elif mode == "animation":
            # TODO: implement the animation mode
            raise NotImplementedError

    def __eq__(self, __value: Any) -> bool:
        if isinstance(__value, INTERACTIONCase):
            return (
                self.location == __value.location
                and self.case_id == __value.case_id
            )
        return NotImplemented

    def __ne__(self, __value: Any) -> bool:
        if isinstance(__value, INTERACTIONCase):
            return (
                self.location != __value.location
                or self.case_id != __value.case_id
            )
        return NotImplemented

    def __ge__(self, __value: Any) -> bool:
        if (
            isinstance(__value, INTERACTIONCase)
            and self.location == __value.location
        ):
            return self.case_id >= __value.case_id
        return NotImplemented

    def __gt__(self, __value: Any) -> bool:
        if (
            isinstance(__value, INTERACTIONCase)
            and self.location == __value.location
        ):
            return self.case_id > __value.case_id
        return NotImplemented

    def __le__(self, __value: Any) -> bool:
        if (
            isinstance(__value, INTERACTIONCase)
            and self.location == __value.location
        ):
            return self.case_id <= __value.case_id
        return NotImplemented

    def __lt__(self, __value: Any) -> bool:
        if (
            isinstance(__value, INTERACTIONCase)
            and self.location == __value.location
        ):
            return self.case_id < __value.case_id
        return NotImplemented

    def __hash__(self) -> int:
        return hash(
            (
                self.location,
                self.case_id,
                self.history_tracks,
                self.current_tracks,
                self.futural_tracks,
                self.tracks_to_predict,
                self.interesting_agents,
            )
        )

    def __str__(self) -> str:
        attr_str = ", ".join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"<{self.__class__.__name__}({attr_str}) at {hex(id(self))}>"

    def __repr__(self) -> str:
        return str(self)
