# Copyright (c) Meta Platforms, Inc. and affiliates.

"""
Wrapper around the vpdq signal type.
"""

from .vpdq_util import (
    VPDQ_INDEX_MATCH_THRESHOLD_PERCENT,
    VpdqCompactFeature,
    json_to_vpdq,
    vpdq_to_json,
    VPDQ_DISTANCE_THRESHOLD,
    VPDQ_QUERY_MATCH_THRESHOLD_PERCENT,
    VPDQ_QUALITY_THRESHOLD,
    hash_file_compact,
)
from .vpdq_brute_matcher import match_VPDQ_hash_brute
import pathlib
import typing as t
#from threatexchange.content_type.content_base import ContentType
#from threatexchange.content_type.video import VideoContent
#from threatexchange.signal_type import signal_base
#from threatexchange.signal_type.pdq.signal import PdqSignal
#from .vpdq_index import VPDQSimilarityInfo, VPDQIndex


class VPDQSignal:
    """
    Simple signal type for video using VPDQ.
    VPDQ signal_str is the json serialization from a list of VPDQ features
    The json serialization will convert the the list of VPDQ features to list of json objects
    where frame_number is the key:
    {(frame_number)
        0: {
            "quality": 100,
            "hash": PDQHash,
            "timestamp": 0.0
            },

        1: {
            "quality": 100,
            "hash": Hash256,
            "timestamp": 0.1
            },
            ...
    }
    Read about VPDQ at https://github.com/facebook/ThreatExchange/tree/main/vpdq
    """

    @classmethod
    def validate_signal_str(cls, signal_str: str) -> str:
        """
        @see VpdqCompactFeature
        """
        json_to_vpdq(signal_str)  # throws value error on failure
        return signal_str

    @classmethod
    def hash_from_file(cls, path: pathlib.Path, seconds_per_hash: float = 1) -> str:
        return vpdq_to_json(hash_file_compact(str(path), seconds_per_hash))

    @classmethod
    def get_similarity(
        cls,
        hash1: str,
        hash2: str,
        ):
            vpdq_hash1 = json_to_vpdq(hash1)
            vpdq_hash2 = json_to_vpdq(hash2)
            match_percent = match_VPDQ_hash_brute(
                vpdq_hash1,
                vpdq_hash2,
                VPDQ_QUALITY_THRESHOLD,
                VPDQ_DISTANCE_THRESHOLD,
            )

            assert match_percent.query_match_percent >= 0 and match_percent.compared_match_percent >= 0
            return match_percent.query_match_percent, match_percent.compared_match_percent
