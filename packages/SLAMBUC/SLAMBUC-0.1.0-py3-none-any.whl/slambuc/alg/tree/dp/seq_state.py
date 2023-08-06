# Copyright 2023 Janos Czentye
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import math

import networkx as nx

from slambuc.alg import INFEASIBLE
from slambuc.alg.tree import seq_tree_partitioning
from slambuc.alg.util import recalculate_partitioning
from slambuc.gen.transform import transform_autonomous_caching


def cacheless_chain_partitioning(tree: nx.DiGraph, root: int = 1, M: int = math.inf, N: int = 1, L: int = math.inf,
                                 cp_end: int = None, delay: int = 1, valid: bool = True) -> tuple[list[int], int, int]:
    partition, *_ = seq_tree_partitioning(tree, root, M, N, L, cp_end, delay, unit=1)
    if not partition:
        return INFEASIBLE
    sum_cost, sum_lat = recalculate_partitioning(tree, partition, root, N, cp_end, delay)
    return INFEASIBLE if valid and sum_lat > L else (partition, sum_cost, sum_lat)


def stateful_chain_partitioning(tree: nx.DiGraph, root: int = 1, M: int = math.inf, N: int = 1, L: int = math.inf,
                                cp_end: int = None, delay: int = 1) -> tuple[list[int], int, int]:
    partition, *_ = seq_tree_partitioning(transform_autonomous_caching(tree, root, copy=True),
                                          root, M, N, L, cp_end, delay, unit=1)
    return (partition, *recalculate_partitioning(tree, partition, root, N, cp_end, delay)) if partition else INFEASIBLE
