import unittest
from fggs.domains import *
from fggs.factors import *
from fggs.fggs import *
from fggs.fgg_utils import *

class TestSingleton(unittest.TestCase):

    def setUp(self):
        self.nl1   = NodeLabel("nl1")
        self.node1 = Node(self.nl1)
        self.node2 = Node(self.nl1)
        
        self.el1   = EdgeLabel("el1", (self.nl1, self.nl1), is_terminal=True)
        self.edge1 = Edge(self.el1, (self.node1, self.node2))
        
        self.graph = Graph()
        self.graph.add_node(self.node1)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.edge1)
        self.graph.ext = [self.node1]
        
        self.start = EdgeLabel("<S>", [self.nl1], is_nonterminal=True)
        
    def test_singleton_hrg(self):
        g = singleton_hrg(self.graph)
        self.assertCountEqual(g.node_labels(), [self.nl1])
        self.assertCountEqual(g.edge_labels(), [self.el1, self.start])
        self.assertEqual(g.start_symbol, self.start)
        self.assertEqual(len(g.all_rules()), 1)
    
    def test_unique_start_name(self):
        s1_lab  = EdgeLabel("<S>", [], is_terminal=True)
        s2_lab  = EdgeLabel("<<S>>", [], is_terminal=True)
        s1_edge = Edge(s1_lab, [])
        s2_edge = Edge(s2_lab, [])
        self.graph.add_edge(s1_edge)
        self.graph.add_edge(s2_edge)
        
        g = singleton_hrg(self.graph)
        self.assertEqual(g.start_symbol.name, "<<<S>>>")
