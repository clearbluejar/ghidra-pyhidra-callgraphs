import argparse
from pathlib import Path
import re

import pyhidra
pyhidra.start(True)

from typing import List, Union, Tuple, TYPE_CHECKING

# needed for ghidra python vscode autocomplete
if TYPE_CHECKING:
    import ghidra
    from ghidra_builtins import *

# Java imports ()
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.program.model.listing import Function

class CallGraph:
    def __init__(self,root=None):
        self.graph = {}
        self.mind = []
        self.title = None
        self.root = root
        self.count = 0

    def set_root(self, root: str):
        self.root = root

    def add_edge(self, node1, node2, depth):

        self.graph.setdefault(node1, [])
        self.graph.setdefault(node2, [])

        self.graph[node1].append((node2, depth, self.count))
        self.count += 1

    def print_graph(self):
        for source, destination in self.graph.items():
            print(f"{source}-->{destination}")

    def get_entrypoints(self) -> list:

        entrypoints = set()

        destinations = []
        
        for src,dst in self.graph.items():
        
            # special case of loop
            if len(dst) == 1 and dst[0] == src:
                # don't append to destinations in this case
                continue
                
        
            for d in dst:
                destinations.append(d[0])

        entrypoints = set(self.graph.keys()).difference(set(destinations))

        return list(entrypoints)

    def depth_count(self, depth: int) -> int:
        """
        Returns count for nodes at a specific depth
        """

        count = 0
        for src,dst in self.graph.items():

            for d in dst:
                if d[1] == depth:
                    count += 1

        return count


    def gen_mermaid_flow_graph(self, direction='TD', shade_nodes : list = []) -> str:
        """
        Generate MermaidJS flowchart from self.graph
        See https://mermaid.js.org/syntax/flowchart.html
        """

        # TODO mark root node with circle
        # TODO mark entrypoints with shape
        # TODO add ability to shade specific nodes

        node_keys = {}
        node_count = 0

        mermaid_flow = '''flowchart {direction}\n{links}\n'''

        if len(self.graph) == 0:
            links = [str(self.root)]
        else:            
            links = set()
        
        for src, dst in self.graph.items():

            for node in dst:
                if node_keys.get(node[0]) is None:
                    node_keys[node[0]] = node_count
                    node_count += 1

                if node_keys.get(src) is None:
                    node_keys[src] = node_count
                    node_count += 1
                
                link = f'{node_keys[src]}["{src}"] --> {node_keys[node[0]]}["{node[0]}"]'
                links.add(link)
                   
            # link = f"{src} --> {node[0]}"
            # links.add(link.replace('~', 'dtor_'))

        return mermaid_flow.format(links='\n'.join(set(links)), direction=direction)


    def gen_mermaid_mind_map(self) -> str:
        """
        Generate MermaidJS mindmap from self.graph
        See https://mermaid.js.org/syntax/mindmap.html
        """

        rows = []

        mermaid_mind = '''mindmap\nroot(({root}))\n{rows}\n'''

        destinations = []

        for src,dst in self.graph.items():
            for d in dst:
                destinations.append(d)

        last_depth = 0
        current_level_names = []
        for i,row in enumerate(sorted(destinations,key=lambda x: x[2])):
            depth = row[1]            

            # skip root row
            if depth < 2:                
                continue

            if depth < last_depth:
                # reset level names
                current_level_names = []

            if not row[0] in current_level_names:
                spaces = (depth+1)*'  '
                rows.append(f"{spaces}{row[0]}")
                last_depth = depth
                current_level_names.append(row[0])
            

            # handle root node
            

        return mermaid_mind.format(rows='\n'.join(rows), root=self.root)        

MAX_DEPTH = 10000
monitor = ConsoleTaskMonitor()

# Recursively calling to build calling graph
def get_calling(f: Function, cgraph: CallGraph = CallGraph(), depth: int = 0, entry_points: list = [], visited: list = []):
    """
    Build a call graph of all calling functions
    Traverses depth first
    """

    if f == None:
        return None

    if depth == 0:        
        print(f"root({f.getName(True)})")
        #cgraph.mind.append(f"root({f.getName(True)})")
        cgraph.set_root(f.getName(True))
    # Traverse through to MAX_DEPTH
    elif depth > MAX_DEPTH:
        return cgraph
    
    space = (depth+2)*'  '
    
    # loop check
    if [f.entryPoint.toString(), f.getName(True)] in visited:
        
        # calling loop
        print(f"{space} - LOOOOP {f.getName(True)}")
        cgraph.mind.append(f"{space} LOOOOP {f.getName(True)}")

        # mark start_point
        entry_points.append([depth, f"LOOOOP {f.getName(True)}"])

        # add ref to self
        cgraph.add_edge(f.getName(), f.getName(), depth)
        
        return cgraph

    calling = f.getCallingFunctions(monitor)

    visited.append([f.entryPoint.toString(), f.getName(True)])

    if len(calling) != 0:

        currently_visited = visited.copy()
        depth = depth+1

        for c in calling:

            # Add calling edge
            cgraph.add_edge(c.getName(), f.getName(), depth)

            cgraph.mind.append(f"{space}{c.getName()}")

            if c.isExternal():
                print(f"{space} - {c.getExternalLocation().getLibraryName()} name {c.getName(False)} ")
            else:
                print(f"{space} - {c.getName()}")

            # Parse further functions
            cgraph = get_calling(c, cgraph, depth,  entry_points, currently_visited)

    else:
        entry_points.append([depth, f.getName(False)])

    return cgraph

def _wrap_mermaid(text: str) -> str:
    return f'''```mermaid\n{text}\n```'''

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='A demo Ghidra callgraph generation script')

    parser.add_argument('bin', help='Path to binary used for analysis')

    parser.add_argument('--include',  action='append',help='Filter name or partial name of function to graph.')
    parser.add_argument('-s', '--symbol-path',
                        dest='symbol_path', help='Path to symbol path for bin')
    parser.add_argument('-o', '--output-path', dest="output_path",
                        help='Callgraph output directory. WinBinDiff Output Path', default='.callgraphs')

    args = parser.parse_args()

    print(args)

    bin_path = Path(args.bin)
    cgraph_name = bin_path.name
    project_location = Path('.ghidra_projects')
    output_path = Path(args.output_path) / bin_path.name
    output_path.mkdir(exist_ok=True,parents=True)

with pyhidra.open_program(bin_path, project_location=project_location, project_name=bin_path.name,analyze=False) as flat_api:

    from ghidra.program.util import GhidraProgramUtilities
    from ghidra.app.script import GhidraScriptUtil
    from ghidra.base.project import GhidraProject

    program : "ghidra.program.model.listing.Program" = flat_api.getCurrentProgram()
    #project = GhidraProject.openProject(project_location + '_ghidra', bin_path.name + '_ghidra', True)

    # configure symbol path for bin
    if args.symbol_path:
        symbol_path = Path(args.symbol_path)
        from ghidra.app.plugin.core.analysis import PdbUniversalAnalyzer
        from java.io import File

        pdbFile = File(symbol_path)
        PdbUniversalAnalyzer.setPdbFileOption(program, pdbFile)

    # analyze program if we haven't yet
    if GhidraProgramUtilities.shouldAskToAnalyze(program):        
        GhidraScriptUtil.acquireBundleHostReference()
        flat_api.analyzeAll(program)
        GhidraProgramUtilities.setAnalyzedFlag(program, True)
        GhidraScriptUtil.releaseBundleHostReference()

    all_funcs = program.functionManager.getFunctions(True)

    for f in all_funcs:

        if args.include:
            if not any([match.lower() in f.getName(True).lower() for match in args.include]):
                # skip functions that don't match any of the include args
                continue

        entry_points = []
        visited = []

        cgraph = CallGraph()
        cgraph = get_calling(f,cgraph, entry_points=entry_points, visited=visited)
        
        print(entry_points)
        
        flow = cgraph.gen_mermaid_flow_graph()
        print(flow)
        mind = cgraph.gen_mermaid_mind_map()        
        print(mind)
        
        skip_output = []
        
        if len(cgraph.graph) > 5:

            print(flow)
            print(mind)
            print(cgraph.get_entrypoints())

            file_name = re.sub(r'[^\w_. -]', '_', f.getName())

            if len(file_name) > 15:
                skip_output.append([f.getName(True), len(file_name)])
            else:
                graph_path = output_path / Path(file_name + '.flow.md')
                mind_path = output_path / Path(file_name + '.mind.md')
                graph_path.write_text(_wrap_mermaid(flow))
                mind_path.write_text(_wrap_mermaid(mind))
        else:
            print(f"Skipping out for short graph {f.getName(True)}")


        if cgraph.depth_count(2) > 10:
            print(mind)
