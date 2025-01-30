from modules import ScoringEngine
import unittest


class TestScoringEngine(unittest.TestCase):
    def setUp(self):
        self.scoring_engine = ScoringEngine()
        self.sample_response = """
        I believe technology has dramatically changed the way we live and work. 
        For instance, smartphones have made communication instant and seamless. 
        However, there are both advantages and disadvantages to consider.
        """
        self.audio_duration = 20.0  # 20 seconds sample

    def test_score_fluency(self):
        score = self.scoring_engine._score_fluency(
            self.sample_response, self.audio_duration)
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 9)

    def test_score_lexical(self):
        score = self.scoring_engine._score_lexical(self.sample_response)
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 9)

    def test_score_grammar(self):
        score = self.scoring_engine._score_grammar(self.sample_response)
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 9)

    def test_score_pronunciation(self):
        score = self.scoring_engine._score_pronunciation(self.sample_response)
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 9)

    def test_full_evaluation(self):
        result = self.scoring_engine.evaluate_response(
            self.sample_response, self.audio_duration)

        self.assertIn('scores', result)
        self.assertIn('feedback', result)
        self.assertIn('overall_score', result)

        for criterion in ['fluency', 'lexical', 'grammar', 'pronunciation']:
            self.assertIn(criterion, result['scores'])
            self.assertIn(criterion, result['feedback'])


if __name__ == '__main__':
    unittest.main()
