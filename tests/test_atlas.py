import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from distributed_memory_atlas.core import Experiment, generate_random_token
from distributed_memory_atlas.approaches import combinatorial,spectral,probabilistic,sheaf,information,comparison,exploration,crypto_lab

class AtlasTests(unittest.TestCase):
    def setUp(self):
        self.e=Experiment(name='test',token=[1,2,3,4,5,6],field_projection=[1,2,3,4,5,6],p=101,mode='M',region_limit=14,max_dim=2)
    def test_generators_reproducible(self):
        for typ in ['chars','words','integers','natural_numbers','vectors','cyclic_permutations','functions']:
            a=generate_random_token(5,typ,seed=9,p=101,object_dimension=4)
            b=generate_random_token(5,typ,seed=9,p=101,object_dimension=4)
            self.assertEqual(a,b);self.assertEqual(len(a['token']),5);self.assertTrue(all(0<=x<101 for x in a['field_projection']))
    def test_experiment_regenerate(self):
        self.e.regenerate(dimension=7,token_type='words',seed=3)
        self.assertEqual(self.e.n,7);self.assertEqual(len(self.e.field_projection),7)
    def test_combinatorial_rank(self):
        a=combinatorial.analyze(self.e)
        self.assertEqual(a['summary']['rank_over_field'],self.e.n)
        self.assertEqual(a['summary']['data_regions'],self.e.n)
    def test_binary_distance(self):
        e=Experiment(token=[1,2,3,4,5],field_projection=[1,2,3,4,5],p=2,mode='Q')
        a=combinatorial.analyze(e)
        self.assertGreaterEqual(a['coding']['minimum_distance_binary']['distance'],1)
    def test_spectral_projective_rank(self):
        a=spectral.analyze(self.e)
        self.assertEqual(a['summary']['constraint_rank'],self.e.n-1)
        self.assertTrue(a['summary']['projectively_recoverable'])
    def test_spectral_tda(self):
        a=spectral.analyze(self.e)
        self.assertIn('betti',a['tda'])
    def test_probability_endpoints(self):
        a=probabilistic.analyze(self.e,q=1.0,trials=100,seed=1)
        self.assertEqual(a['systematic']['recovery_probability'],1.0)
        self.assertEqual(a['spectral']['recovery_probability'],1.0)
        b=probabilistic.analyze(self.e,q=0.0,trials=100,seed=1)
        self.assertEqual(b['systematic']['recovery_probability'],0.0)
        self.assertEqual(b['spectral']['recovery_probability'],0.0)
    def test_sheaf_gluing(self):
        a=sheaf.analyze(self.e)
        self.assertTrue(a['compatibility']['compatible'])
        self.assertGreaterEqual(a['cohomology']['cohomology_dimensions'][0],1)
    def test_information_rank_identity(self):
        a=information.analyze(self.e,trials=100)
        r=a['summary']['rank'];expected=r*__import__('math').log2(self.e.p)
        self.assertAlmostEqual(a['summary']['capacity_bits'],expected)
    def test_comparison_bridge(self):
        a=comparison.analyze(self.e,trials=100)
        self.assertTrue(a['bridge_invariants']['rank_information_identity_holds'])
        self.assertTrue(a['bridge_invariants']['sheaf_compatible'])
        self.assertEqual(len(a['rows']),5)
    def test_legacy_permutation_import_shape(self):
        token=[[0,1,2],[1,2,0],[2,0,1],[0,2,1],[2,1,0],[1,0,2]]
        e=Experiment.from_payload({'token':token,'aggregation':'compose','mode':'Q','p':101})
        self.assertEqual(e.n,6)
        self.assertEqual(len(e.field_projection),6)
        self.assertEqual(e.aggregation,'compose')

    def test_exploration_geometry_all_lenses(self):
        for lens in ["combinatorial","spectral","probabilistic","sheaf","information"]:
            g=exploration.geometry_payload(self.e,lens,q=.85,limit=12)
            self.assertEqual(len(g["coordinates"]),self.e.n)
            self.assertGreater(g["total"],0)
            self.assertLessEqual(len(g["regions"]),12)

    def test_exploration_graph_all_lenses(self):
        for lens in ["combinatorial","spectral","probabilistic","sheaf","information"]:
            g=exploration.graph_payload(self.e,lens,q=.8,limit=100)
            self.assertEqual(len([n for n in g["nodes"] if n["kind"]=="coordinate"]),self.e.n)
            self.assertTrue(all("source" in edge and "target" in edge for edge in g["edges"]))

    def test_spectral_geometry_has_virtual_regions_under_rank_basis(self):
        g=exploration.geometry_payload(self.e,"spectral",limit=100)
        self.assertGreater(g["summary"]["virtual"],0)
        self.assertEqual(g["summary"]["physical"] , spectral.analyze(self.e)["summary"]["physical_regions"])

    def test_region_details_all_lenses(self):
        for lens in ["combinatorial","spectral","probabilistic","sheaf","information"]:
            d=exploration.region_detail(self.e,lens,1,q=.9)
            self.assertEqual(d["id"],1)
            self.assertIn("meaning",d)

    def test_crypto_lab_rank_invariance_all_lenses(self):
        for lens in ["combinatorial","spectral","probabilistic","sheaf","information"]:
            c=crypto_lab.analyze(self.e,lens,key="test-key",visible_fraction=.5)
            self.assertTrue(c["transform"]["rank_invariant"])
            self.assertTrue(c["transform"]["roundtrip_recovers_original"])
            self.assertIn("security_warning",c)

    def test_sheaf_crypto_preserves_cohomology_under_relabeling(self):
        c=crypto_lab.analyze(self.e,"sheaf",key="topology-key",visible_fraction=.5)
        self.assertTrue(c["transform"]["cohomology_invariant"])

    def test_information_crypto_matches_rank_information(self):
        import math
        c=crypto_lab.analyze(self.e,"information",key="info-key",visible_fraction=.6)
        a=c["access_structure"]
        self.assertAlmostEqual(a["mutual_information_bits_uniform_source"],a["observation_rank"]*math.log2(self.e.p))

if __name__=='__main__':unittest.main()
