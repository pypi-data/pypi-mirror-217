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
import itertools
import os
import pathlib
import subprocess
import tempfile

import networkx as nx
import pulp
import tabulate

from slambuc.alg import LP_LAT
from slambuc.alg.service.common import *
from slambuc.alg.util import (ichain, path_blocks, block_memory, block_cost, block_latency, leaf_label_nodes, block_cpu,
                              ser_block_subcost, ser_block_sublatency, ser_block_submemory, ser_subtree_cost,
                              ser_subchain_latency, par_subtree_cost, par_subchain_latency)
from slambuc.misc.plot import draw_tree


def get_cplex_path():
    if isinstance(cp := subprocess.run(['which', 'cplex']), str):
        return cp
    return str(pathlib.Path(os.environ.get('CPLEX_HOME', '~/Programs/ibm/ILOG/CPLEX_Studio2211/cplex'),
                            'bin/x86-64_linux/cplex').expanduser())


def get_cpo_path():
    if isinstance(cp := subprocess.run(['which', 'cpoptimizer']), str):
        return cp
    return str(pathlib.Path(os.environ.get('CPO_HOME', '~/Programs/ibm/ILOG/CPLEX_Studio2211/cpoptimizer'),
                            'bin/x86-64_linux/cpoptimizer').expanduser())


def is_compatible(tree1: nx.DiGraph, tree2: nx.DiGraph) -> bool:
    """Return true if given second *tree2* has the same structure and edge/node attributes as the first *tree1*"""
    return (nx.is_isomorphic(tree1, tree2) and
            all(all(tree1[u][v][a] == tree2[u][v][a] for a in tree1[u][v]) and
                all(tree1.nodes[v][a] == tree2.nodes[v][a] for a in tree1.nodes[v]) for u, v in tree1.edges))


def get_chain_k_min(memory: list[int], M: int, rate: list[int], N: int, start: int = 0, end: int = None) -> int:
    """Return minimal number of blocks due to constraint M and N"""
    end = end if end is not None else len(memory) - 1
    return max(math.ceil(block_memory(memory, start, end) / M),
               sum(1 for i, j in itertools.pairwise(rate[start: end + 1]) if math.ceil(j / i) > N))


def get_chain_c_min(memory: list[int], M: int, rate: list[int], N: int, start: int = 0, end: int = None) -> int:
    """Return minimal number of cuts due to constraint M and N"""
    return get_chain_k_min(memory, M, rate, N, start, end) - 1


def get_chain_c_max(runtime: list[int], L: int, b: int, w: int, delay: int, start: int = 0, end: int = None) -> int:
    """Return maximal number of blocks due to constraint L"""
    end = end if end is not None else len(runtime) - 1
    return math.floor(min((L - block_latency(runtime, b, w, delay, start, end)) / delay, len(runtime) - 1))


def get_chain_k_max(runtime: list[int], L: int, b: int, w: int, delay: int, start: int = 0, end: int = None) -> int:
    """Return maximal number of blocks due to constraint L"""
    return get_chain_c_max(runtime, L, b, w, delay, start, end) + 1


def get_chain_k_opt(partition: list[list[int]], start: int = 0, end: int = None) -> int:
    """Return the number of blocks included by the [start, end] interval in partitioning"""
    end = end if end is not None else partition[-1][-1]
    cntr = 0
    in_chain = False
    for blk in partition:
        b, w = blk[0], blk[-1]
        if not in_chain and b <= start:
            in_chain = True
        if in_chain:
            cntr += 1
        if in_chain and end <= w:
            in_chain = False
    return cntr


def get_chain_c_opt(partition: list[list[int]], start: int = 0, end: int = None) -> int:
    """Return the number of cuts included by the [start, end] interval in partitioning"""
    return get_chain_k_opt(partition, start, end) - 1


def prune_chain(tree: nx.DiGraph, node: int, leaf: int) -> tuple[list[int], list[int]]:
    """Return the nodes of chain [node, leaf] and the branching nodes"""
    chain = [node]
    branches = []
    u = node
    while u != leaf:
        for _, v in tree.out_edges(u):
            if leaf in tree.nodes[v][LABEL]:
                chain.append(v)
            else:
                branches.append(v)
        u = chain[-1]
    return chain, branches


########################################################################################################################


def print_chain_summary(runtime: list[int], memory: list[int], rate: list[int]):
    print("Chain:", "[", *(f"-{r}-> F({t}|M{m})" for t, m, r in zip(runtime, memory, rate)), "]")


def evaluate_chain_partitioning(partition: list, opt_cost: int, opt_lat: int, runtime: list, memory: list, rate: list,
                                M: int = math.inf, N: int = math.inf, L: int = math.inf, start: int = 0,
                                end: int = None, delay: int = 1, unit: int = 100):
    print('#' * 80)
    print(f"Chain partitioning [M={M}, N={N}, L={L}:{(start, end)}] => "
          f"{partition} - opt_cost: {opt_cost}, opt_lat: {opt_lat}")
    print(f"k_min={get_chain_k_min(memory, M, rate, N, start, end)}, "
          f"k_opt[L]={len(path_blocks(partition, range(start, end + 1)))}, "
          f"k_max={get_chain_k_max(runtime, L, 0, len(runtime), delay, start, end)}")
    print_block_stat(partition, runtime, memory, rate, delay, start, end, unit)
    print('#' * 80)


def print_block_stat(partition: list[list[int]], runtime: list[int], memory: list[int], rate: list[int], delay: float,
                     start: int = 0, end: int = None, unit: int = 100):
    end = end if end is not None else len(runtime) - 1
    stat = [[str([blk[0], blk[-1]]),
             block_cost(runtime, rate, blk[0], blk[-1], unit),
             block_memory(memory, blk[0], blk[-1]),
             block_cpu(rate, blk[0], blk[-1]),
             block_latency(runtime, blk[0], blk[-1], delay, start, end)] for blk in partition]
    print(tabulate.tabulate(stat, ['Block', 'Cost', 'Memory', 'CPU', 'Latency'],
                            numalign='decimal', stralign='center', tablefmt='pretty'))


def print_chain_partition_result(barr: list[int], cost: int, lat: int):
    if barr is not None:  # [], cost, lat
        print("Minimal-cost solution is calculated.")
    elif cost is not None and lat is None:  # None, inf, None
        print("Feasible latency-fitting solution cannot be generated due to memory constraint M.")
    elif cost is None and lat is not None:  # None, None, lat
        print("Solution does not exist due to too strict latency constraint L.")
    else:  # None, None, None
        print("Feasible solution does not exist due to non-overlapping constrains L and M.")


def print_tree_summary(tree: nx.DiGraph):
    """Print summary of service graphs"""
    print(tree)
    for n, nd in tree.nodes(data=True):
        print(f"\t{n}: {nd}")
        for i, j, ed in tree.out_edges(n, data=True):
            print(f"\t\t{i} -> {j}: {ed}")


def print_tree_block_stat(tree: nx.DiGraph, partition: list[list[int]], unit: int = 100):
    """Print cost memory and latency values of partition blocks in tabulated format"""
    stat = []
    for blk in partition:
        pred = next(tree.predecessors(blk[0]))
        runtime, memory, rate = zip(*[(tree.nodes[v][RUNTIME], tree.nodes[v][MEMORY], tree[u][v][RATE])
                                      for u, v in itertools.pairwise([pred] + blk)])
        b, w = 0, len(blk) - 1
        stat.append([str([blk[b], blk[w]]),
                     block_cost(runtime, rate, b, w, unit),
                     block_memory(memory, b, w),
                     block_cpu(rate, b, w),
                     block_latency(runtime, b, w, 0, b, w)])
    print(tabulate.tabulate(stat, ['Block', 'Cost', 'Memory', 'CPU', 'Latency'], numalign='decimal', stralign='center'))


def print_cpath_stat(tree: nx.DiGraph, partition: list[list[int]], cpath: list[int] = None, delay: int = 10):
    """Print the related block of the critical path and """
    if len(partition) > 0:
        c_blocks = path_blocks(partition, cpath)
        opt_cut = len(c_blocks) - 1
        sum_lat = sum(block_latency([tree.nodes[v][RUNTIME] for v in blk], 0, len(blk) - 1, delay, 0, len(blk) - 1)
                      for blk in c_blocks) + opt_cut * delay
        print("Critical blocks of cpath", [cpath[0], cpath[-1]], "=>", c_blocks, "-", "opt_cut:", opt_cut, "-",
              "opt_lat:", sum_lat)


def evaluate_tree_partitioning(tree: nx.DiGraph, partition: list[list[int]], opt_cost: int, root: int, cp_end: int,
                               M: int, N: int, L: int, delay: int, unit: int):
    tree = leaf_label_nodes(tree)
    print(tree.graph.get(NAME, "tree").center(80, '#'))
    print("Runtime:", [tree.nodes[v][RUNTIME] for v in tree.nodes if v is not PLATFORM])
    print("Memory:", [tree.nodes[v][MEMORY] for v in tree.nodes if v is not PLATFORM])
    print("Rate:", [tree[next(tree.predecessors(v))][v][RATE] for v in tree.nodes if v is not PLATFORM])
    print(f"Tree partitioning [M={M}, N={N}, L={L}:{(root, cp_end)}] => {partition} - opt_cost: {opt_cost}")
    if partition:
        print_cpath_stat(tree, partition, list(ichain(tree, root, cp_end)), delay)
        print_tree_block_stat(tree, partition, unit)
        draw_tree(tree, partition, draw_blocks=True, draw_weights=False)
    print('#' * 80)


########################################################################################################################


def print_ser_tree_block_stat(tree: nx.DiGraph, partition: list[list[int]], cpath: list[int]):
    """Print cost memory and latency values of partition blocks in tabulated format"""
    stat = []
    for blk in partition:
        blk_cost = ser_subtree_cost(tree, blk[0], blk)
        blk_lat = ser_subchain_latency(tree, blk[0], set(blk), set(cpath))
        stat.append([str([blk[0], blk[-1]]), blk_cost, sum(tree.nodes[v][MEMORY] for v in blk), blk_lat])
    print(tabulate.tabulate(stat, ['Block', 'Cost', 'Memory', 'Latency'], numalign='decimal', stralign='center'))


def print_ser_cpath_stat(tree: nx.DiGraph, partition: list[list[int]], cpath: list[int] = None, delay: int = 10):
    """Print the related block of the critical path"""
    cpath = set(cpath)
    if len(partition) > 0:
        restricted_blk = [blk for blk in partition if blk[0] in cpath]
        blk_lats = [ser_subchain_latency(tree, blk[0], set(blk), cpath) for blk in restricted_blk]
        sum_lat = sum(blk_lats) + (len(restricted_blk) - 1) * delay
        print("Critical blocks wrt. cpath:", sorted(cpath), "=>", restricted_blk, "-", "opt_lat:", sum_lat)


def evaluate_ser_tree_partitioning(tree: nx.DiGraph, partition: list[list[int]], opt_cost: int, opt_lat: int,
                                   root: int, cp_end: int, M: int, L: int, delay: int, draw: bool = True):
    tree = leaf_label_nodes(tree)
    print(tree.graph.get(NAME, "tree").center(80, '#'))
    print("Runtime:", [tree.nodes[v][RUNTIME] for v in tree.nodes if v is not PLATFORM])
    print("Memory:", [tree.nodes[v][MEMORY] for v in tree.nodes if v is not PLATFORM])
    print("Data:", [tree[next(tree.predecessors(v))][v][DATA] for v in tree.nodes if v is not PLATFORM])
    print("Rate:", [tree[next(tree.predecessors(v))][v][RATE] for v in tree.nodes if v is not PLATFORM])
    print(f"Tree partitioning [M={M}, L={L}:{(root, cp_end)}] => {partition} - opt_cost: {opt_cost},"
          f" opt_lat: {opt_lat}")
    if partition:
        print_ser_cpath_stat(tree, partition, list(ichain(tree, root, cp_end)), delay)
        print(f"Recalculated partition cost: {sum(ser_subtree_cost(tree, blk[0], blk) for blk in partition)}")
        print_ser_tree_block_stat(tree, partition, set(ichain(tree, root, cp_end)))
        if draw:
            draw_tree(tree, partition, draw_blocks=True, draw_weights=False)
    print('#' * 80)


def print_par_tree_block_stat(tree: nx.DiGraph, partition: list[list[int]], cpath: list[int], N: int = 1):
    """Print cost memory and latency values of partition blocks in tabulated format"""
    stat = []
    for blk in partition:
        blk_cost = par_subtree_cost(tree, blk[0], blk, N)
        blk_lat = par_subchain_latency(tree, blk[0], set(blk), set(cpath), N)
        stat.append([str([blk[0], blk[-1]]), blk_cost, sum(tree.nodes[v][MEMORY] for v in blk), blk_lat])
    print(tabulate.tabulate(stat, ['Block', 'Cost', 'Memory', 'Latency'], numalign='decimal', stralign='center'))


def print_par_cpath_stat(tree: nx.DiGraph, partition: list[list[int]], cpath: list[int] = None, delay: int = 10,
                         N: int = 1):
    """Print the related block of the critical path"""
    cpath = set(cpath)
    if len(partition) > 0:
        restricted_blk = [blk for blk in partition if blk[0] in cpath]
        blk_lats = [par_subchain_latency(tree, blk[0], set(blk), cpath, N) for blk in restricted_blk]
        sum_lat = sum(blk_lats) + (len(restricted_blk) - 1) * delay
        print("Critical blocks wrt. cpath:", sorted(cpath), "=>", restricted_blk, "-", "opt_lat:", sum_lat)


def evaluate_par_tree_partitioning(tree: nx.DiGraph, partition: list[list[int]], opt_cost: int, opt_lat: int,
                                   root: int, cp_end: int, M: int, L: int, N: int, delay: int, draw: bool = True):
    tree = leaf_label_nodes(tree)
    print(tree.graph.get(NAME, "tree").center(80, '#'))
    print("Runtime:", [tree.nodes[v][RUNTIME] for v in tree.nodes if v is not PLATFORM])
    print("Memory:", [tree.nodes[v][MEMORY] for v in tree.nodes if v is not PLATFORM])
    print("Data:", [tree[next(tree.predecessors(v))][v][DATA] for v in tree.nodes if v is not PLATFORM])
    print("Rate:", [tree[next(tree.predecessors(v))][v][RATE] for v in tree.nodes if v is not PLATFORM])
    print(f"Tree partitioning [{M=}, {L=}:{(root, cp_end)}, {N=}] => {partition} - opt_cost: {opt_cost},"
          f" opt_lat: {opt_lat}")
    if partition:
        print_par_cpath_stat(tree, partition, list(ichain(tree, root, cp_end)), delay, N)
        print_par_tree_block_stat(tree, partition, set(ichain(tree, root, cp_end)), N)
        if draw:
            draw_tree(tree, partition, draw_blocks=True, draw_weights=False)
    print('#' * 80)


def evaluate_gen_tree_partitioning(tree: nx.DiGraph, partition: list[list[int]], opt_cost: int, opt_lat: int,
                                   root: int, flavors: list, cp_end: int, L: int, delay: int, draw: bool = True):
    tree = leaf_label_nodes(tree)
    print(tree.graph.get(NAME, "tree").center(80, '#'))
    print("Runtime:", [tree.nodes[v][RUNTIME] for v in tree.nodes if v is not PLATFORM])
    print("Memory:", [tree.nodes[v][MEMORY] for v in tree.nodes if v is not PLATFORM])
    print("Data:", [tree[next(tree.predecessors(v))][v][DATA] for v in tree.nodes if v is not PLATFORM])
    print("Rate:", [tree[next(tree.predecessors(v))][v][RATE] for v in tree.nodes if v is not PLATFORM])
    M, N, cfactor = zip(*flavors)
    print(f"Tree partitioning [{M=}, {L=}:{(root, cp_end)}, {N=}] => {partition} - opt_cost: {opt_cost},"
          f" opt_lat: {opt_lat}")
    if partition:
        # print_par_cpath_stat(tree, partition, list(ichain(tree, root, cp_end)), delay, N)
        # print_par_tree_block_stat(tree, partition, set(ichain(tree, root, cp_end)), N)
        if draw:
            draw_tree(tree, partition, draw_blocks=True, draw_weights=False)
    print('#' * 80)


def print_ser_chain_summary(runtime: list[int], memory: list[int], rate: list[int], data: list[int]):
    print("Chain:", "[", *(f"-{r}-> F(D{d}|T{t}|M{m})" for t, m, r, d in zip(runtime, memory, rate, data)), "]")


def print_ser_block_stat(partition: list[list[int]], runtime: list[int], memory: list[int], rate: list[int],
                         data: list[int], delay: float, start: int = 0, end: int = None):
    end = end if end is not None else len(runtime) - 1
    stat = [[str([blk[0], blk[-1]]),
             ser_block_subcost(runtime, rate, data, blk[0], blk[-1]),
             ser_block_submemory(memory, blk[0], blk[-1]),
             ser_block_sublatency(runtime, rate, data, blk[0], blk[-1], delay, start, end)] for blk in partition]
    print(tabulate.tabulate(stat, ['Block', 'Cost', 'Memory', 'Latency'],
                            numalign='decimal', stralign='center', tablefmt='pretty'))


def evaluate_ser_chain_partitioning(partition: list, opt_cost: int, opt_lat: int, runtime: list, memory: list,
                                    rate: list, data: list, M: int = math.inf, L: int = math.inf, start: int = 0,
                                    end: int = None, delay: int = 1):
    print('#' * 80)
    print(f"Chain partitioning [M={M}, L={L}:{(start, end)}] => "
          f"{partition} - opt_cost: {opt_cost}, opt_lat: {opt_lat}")
    print_ser_block_stat(partition, runtime, memory, rate, data, delay, start, end)
    print('#' * 80)


########################################################################################################################


def print_lp_desc(model: pulp.LpProblem):
    """Print the lp format of the model"""
    with tempfile.TemporaryDirectory() as tmp:
        model.writeLP(f"{tmp}/chain_model.lp")
        with open(f"{tmp}/chain_model.lp") as f:
            print(f.read())


def convert_var_dict(X: dict[int, dict[int]]) -> list[list[pulp.LpVariable]]:
    """Convert dict-of-dict variable matrix into list-of-list format"""
    return [[X[i][j] if j in X[i] else None for j in range(1, i + 1)] for i in sorted(X)]


def print_var_matrix(X: list[list]):
    """Print matrix of decision variables names in tabular format"""
    print(tabulate.tabulate([list(map(lambda x: x if isinstance(x, (int, type(None))) else x.name, x_i)) for x_i in X],
                            missingval="-", numalign='center', stralign='center', tablefmt='outline'))


def print_pulp_matrix_values(X: list[list[pulp.LpVariable]]):
    """Print matrix of decision variables values in tabular format"""
    print(tabulate.tabulate([list(map(lambda x: x if isinstance(x, (int, type(None))) else pulp.value(x), x_i))
                             for x_i in X], missingval="-", numalign='center', stralign='center', tablefmt='outline'))


def print_cplex_matrix_values(X: list[list]):
    """Print matrix of decision variables values in tabular format"""
    print(tabulate.tabulate([list(map(lambda x: x if isinstance(x, (int, type(None))) else round(x.solution_value),
                                      x_i)) for x_i in X],
                            missingval="-", numalign='center', stralign='center', tablefmt='outline'))


def print_cost_coeffs(model: pulp.LpProblem, X: list[list[pulp.LpVariable]]):
    print(tabulate.tabulate([[model.objective.get(x) for x in x_i] for x_i in X],
                            missingval="-", numalign='center', stralign='center', tablefmt='outline'))


def print_lat_coeffs(model: pulp.LpProblem, X: list[list[pulp.LpVariable]]):
    print(tabulate.tabulate([[model.constraints[LP_LAT].get(x) for x in x_i] for x_i in X],
                            missingval="-", numalign='center', stralign='center', tablefmt='outline'))
