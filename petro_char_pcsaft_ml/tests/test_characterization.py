# tests/test_characterization.py

import unittest
import os
import sys
import json
import math # For math.isclose

# --- Path Adjustment ---
current_dir = os.path.dirname(os.path.abspath(__file__)) # tests directory
project_root = os.path.dirname(current_dir) # petro_char_pcsaft_ml directory
src_path = os.path.join(project_root, "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)

# --- Imports from src ---
try:
    from ml_model import ParameterAdjustmentModel
    from characterization import PetroleumCharacterization
except ImportError as e:
    print(f"Error importing modules from 'src': {e}")
    print(f"Attempted to add src_path: {src_path} to sys.path")
    print(f"Current sys.path: {sys.path}")
    raise

# --- Test Data Setup ---
TEST_DATA_DIR = os.path.join(current_dir, "test_data")
DUMMY_PARAMS_FILENAME = "dummy_params.json" # Contains basic m, sigma, epsilon_k for testing initial load
DUMMY_PARAMS_FILEPATH = os.path.join(TEST_DATA_DIR, DUMMY_PARAMS_FILENAME)
NON_EXISTENT_PARAMS_FILEPATH = os.path.join(TEST_DATA_DIR, "non_existent_params.json")

class TestParameterAdjustmentModel(unittest.TestCase):
    """
    Tests for the ParameterAdjustmentModel class (C7+ focus).
    """

    def setUp(self):
        self.model = ParameterAdjustmentModel(model_path=None) # Using placeholder model

    def test_initialization(self):
        """Test that the model initializes without errors."""
        self.assertIsNotNone(self.model, "Model should initialize.")

    def test_predict_output_structure(self):
        """Test the 'predict' method's output structure for C7+ components."""
        sample_input_features = {'API_gravity': 30, 'overall_molecular_weight': 200}
        predictions = self.model.predict(sample_input_features)

        self.assertIsInstance(predictions, list, "Predictions should be a list.")
        self.assertEqual(len(predictions), 5, "Predictions should contain 5 elements (for 5 C7+ pseudo-components).")

        total_mole_fraction = 0.0
        for component_params in predictions:
            self.assertIsInstance(component_params, dict, "Each component's parameters should be a dictionary.")
            self.assertIn("name", component_params)
            self.assertIn("m", component_params)
            self.assertIn("sigma", component_params)
            self.assertIn("epsilon_k", component_params)
            self.assertIn("mole_fraction", component_params) # New key
            self.assertIn("molar_mass", component_params)    # New key

            # Check types of the parameter values
            self.assertIsInstance(component_params["m"], (int, float))
            self.assertIsInstance(component_params["sigma"], (int, float))
            self.assertIsInstance(component_params["epsilon_k"], (int, float))
            self.assertIsInstance(component_params["mole_fraction"], (int, float)) # New type check
            self.assertIsInstance(component_params["molar_mass"], (int, float))    # New type check
            
            total_mole_fraction += component_params["mole_fraction"]

        self.assertTrue(math.isclose(total_mole_fraction, 1.0, rel_tol=1e-9),
                        f"Sum of mole_fractions should be close to 1.0, but was {total_mole_fraction}")


class TestPetroleumCharacterization(unittest.TestCase):
    """
    Tests for the PetroleumCharacterization class (C7+ focus).
    """

    @classmethod
    def setUpClass(cls):
        """Set up resources for all tests in this class."""
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        # dummy_params.json for initial loading test - does not need all C7+ fields
        # as the ML model is responsible for outputting the full C7+ structure.
        dummy_data_content = [
            {"name": "InitialComp1", "m": 1.0, "sigma": 3.0, "epsilon_k": 100.0, "mole_fraction": 0.5, "molar_mass": 100.0},
            {"name": "InitialComp2", "m": 2.0, "sigma": 3.5, "epsilon_k": 150.0, "mole_fraction": 0.5, "molar_mass": 150.0}
        ]
        with open(DUMMY_PARAMS_FILEPATH, 'w') as f:
            json.dump(dummy_data_content, f, indent=2)

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests in this class."""
        if os.path.exists(DUMMY_PARAMS_FILEPATH):
            os.remove(DUMMY_PARAMS_FILEPATH)
        try:
            os.rmdir(TEST_DATA_DIR)
        except OSError:
            pass # Directory might not be empty

    def test_initialization_success(self):
        """Test successful initialization with a valid parameters file."""
        characterizer = PetroleumCharacterization(initial_params_path=DUMMY_PARAMS_FILEPATH)
        self.assertIsNotNone(characterizer, "Characterizer should initialize.")
        self.assertIsNotNone(characterizer.ml_model)
        self.assertIsNone(characterizer.pcsaft_model)
        self.assertEqual(len(characterizer.initial_pseudo_components), 2)
        self.assertEqual(characterizer.initial_pseudo_components[0]["name"], "InitialComp1")
        # Check if new keys are loaded if present in dummy file
        self.assertIn("mole_fraction", characterizer.initial_pseudo_components[0])
        self.assertIn("molar_mass", characterizer.initial_pseudo_components[0])


    def test_initialization_file_not_found(self):
        """Test initialization with a non-existent parameters file."""
        characterizer = PetroleumCharacterization(initial_params_path=NON_EXISTENT_PARAMS_FILEPATH)
        self.assertIsNotNone(characterizer)
        self.assertEqual(characterizer.initial_pseudo_components, [])

    def test_initialization_default_path(self):
        """Test initialization using the default initial_params_path."""
        default_params_path = os.path.join(project_root, "data", "pseudo_components_initial.json")
        if not os.path.exists(default_params_path):
            self.skipTest(f"Default params file {default_params_path} not found, skipping test.")

        characterizer = PetroleumCharacterization(initial_params_path=None) # Uses default path
        self.assertIsNotNone(characterizer)
        self.assertTrue(len(characterizer.initial_pseudo_components) > 0,
                        "Should load components from the default data/pseudo_components_initial.json")
        # Check if the default loaded components have the new keys (they should)
        self.assertIn("mole_fraction", characterizer.initial_pseudo_components[0])
        self.assertIn("molar_mass", characterizer.initial_pseudo_components[0])

    def test_characterize_c7plus_fraction_output_structure(self):
        """Test the return type and top-level keys of characterize_c7plus_fraction."""
        characterizer = PetroleumCharacterization(initial_params_path=DUMMY_PARAMS_FILEPATH)
        sample_whole_fluid_properties = {'API_gravity': 30, 'overall_molecular_weight': 200}
        results = characterizer.characterize_c7plus_fraction(bulk_properties_whole_fluid=sample_whole_fluid_properties)

        self.assertIsInstance(results, dict, "characterize_c7plus_fraction should return a dictionary.")
        self.assertIn("bulk_inputs_whole_fluid", results)
        self.assertIn("predicted_c7plus_parameters", results)
        self.assertIn("pcsaft_outputs_c7plus", results)
        self.assertIn("notes", results)

        self.assertEqual(results["bulk_inputs_whole_fluid"], sample_whole_fluid_properties)

    def test_characterize_c7plus_predicted_parameters_structure(self):
        """Test the structure of 'predicted_c7plus_parameters'."""
        characterizer = PetroleumCharacterization(initial_params_path=DUMMY_PARAMS_FILEPATH)
        sample_whole_fluid_properties = {'API_gravity': 30, 'overall_molecular_weight': 200}
        results = characterizer.characterize_c7plus_fraction(bulk_properties_whole_fluid=sample_whole_fluid_properties)

        predicted_params = results.get("predicted_c7plus_parameters")
        self.assertIsInstance(predicted_params, list)
        self.assertEqual(len(predicted_params), 5,
                         "'predicted_c7plus_parameters' should contain 5 elements (from placeholder ML model).")

        total_mole_fraction = 0.0
        for component_params in predicted_params:
            self.assertIsInstance(component_params, dict)
            self.assertIn("name", component_params)
            self.assertIn("m", component_params)
            self.assertIn("sigma", component_params)
            self.assertIn("epsilon_k", component_params)
            self.assertIn("mole_fraction", component_params) # New key
            self.assertIn("molar_mass", component_params)    # New key
            
            self.assertIsInstance(component_params["mole_fraction"], (int, float))
            self.assertIsInstance(component_params["molar_mass"], (int, float))
            total_mole_fraction += component_params["mole_fraction"]
            
        self.assertTrue(math.isclose(total_mole_fraction, 1.0, rel_tol=1e-9),
                        f"Sum of mole_fractions in predicted_c7plus_parameters should be close to 1.0, but was {total_mole_fraction}")


if __name__ == '__main__':
    unittest.main()
