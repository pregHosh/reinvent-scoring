import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import \
    create_predictive_property_component_regression, create_activity_component_regression
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from unittest_reinvent.fixtures.test_data import PROPANE, BENZENE, ASPIRIN, METAMIZOLE, CELECOXIB, ETHANE


class Test_custom_sum(unittest.TestCase):

    def setUp(self):
        enum = ScoringFunctionComponentNameEnum()
        predictive_property = create_predictive_property_component_regression()
        activity = create_activity_component_regression()
        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score_name",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})
        custom_alerts = ComponentParameters(component_type=enum.CUSTOM_ALERTS,
                                            name="custom_alerts_name",
                                            weight=1.,
                                            smiles=[PROPANE],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=[BENZENE],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_instance = CustomSum(
            parameters=[activity, qed_score, custom_alerts, matching_substructure, predictive_property])

    def test_special_selectivity_multiplicative_no_sigm_trans_1(self):
        score = self.sf_instance.get_final_score(smiles=[CELECOXIB])
        self.assertAlmostEqual(score.total_score[0], 0.456, 3)

    def test_special_selectivity_multiplicative_no_sigm_trans_2(self):
        score = self.sf_instance.get_final_score(smiles=[ETHANE])
        self.assertAlmostEqual(score.total_score[0], 0.157, 3)

    def test_special_selectivity_multiplicative_no_sigm_trans_3(self):
        score = self.sf_instance.get_final_score(smiles=[ASPIRIN])
        self.assertAlmostEqual(score.total_score[0], 0.421, 3)

    def test_special_selectivity_multiplicative_no_sigm_trans_4(self):
        score = self.sf_instance.get_final_score(smiles=[METAMIZOLE])
        self.assertAlmostEqual(score.total_score[0], 0.510, 3)

