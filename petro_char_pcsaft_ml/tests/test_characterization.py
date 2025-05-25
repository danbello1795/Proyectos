# tests/test_characterization.py

import unittest
import os
import sys
import json

# --- Path Adjustment ---
# Adjust the Python path to include the 'src' directory
# This allows the tests to be run from the project root directory (e.g., petro_char_pcsaft_ml/)
# or from the 'tests' directory itself.
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
# Define the directory for test-specific data files
TEST_DATA_DIR = os.path.join(current_dir, "test_data")
DUMMY_PARAMS_FILENAME = "dummy_params.json"
DUMMY_PARAMS_FILEPATH = os.path.join(TEST_DATA_DIR, DUMMY_PARAMS_FILENAME)
NON_EXISTENT_PARAMS_FILEPATH = os.path.join(TEST_DATA_DIR, "non_existent_params.json")

class TestParameterAdjustmentModel(unittest.TestCase):
    """
    Tests for the ParameterAdjustmentModel class.
    """

    def setUp(self):
        self.model = ParameterAdjustmentModel(model_path=None) # Using placeholder model

    def test_initialization(self):
        """Test that the model initializes without errors."""
        self.assertIsNotNone(self.model, "Model should initialize.")
        # The placeholder model prints, we can't easily check that here without capturing stdout
        # or modifying the model. For now, successful instantiation is the main check.

    def test_predict_output_structure(self):
        """Test the 'predict' method's output structure."""
        sample_input_features = {'API_gravity': 30, 'molecular_weight': 200}
        predictions = self.model.predict(sample_input_features)

        self.assertIsInstance(predictions, list, "Predictions should be a list.")
        self.assertEqual(len(predictions), 5, "Predictions should contain 5 elements (for 5 pseudo-components).")

        for component_params in predictions:
            self.assertIsInstance(component_params, dict, "Each component's parameters should be a dictionary.")
            self.assertIn("name", component_params, "Component parameters should have a 'name' key.")
            self.assertIn("m", component_params, "Component parameters should have an 'm' key.")
            self.assertIn("sigma", component_params, "Component parameters should have a 'sigma' key.")
            self.assertIn("epsilon_k", component_params, "Component parameters should have an 'epsilon_k' key.")
            # Check types of the parameter values
            self.assertIsInstance(component_params["m"], (int, float), "'m' should be a number.")
            self.assertIsInstance(component_params["sigma"], (int, float), "'sigma' should be a number.")
            self.assertIsInstance(component_params["epsilon_k"], (int, float), "'epsilon_k' should be a number.")


class TestPetroleumCharacterization(unittest.TestCase):
    """
    Tests for the PetroleumCharacterization class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up resources for all tests in this class.
        Create the dummy parameters file.
        """
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        dummy_data_content = [
            {"name": "TestComp1", "m": 1.0, "sigma": 3.0, "epsilon_k": 100.0},
            {"name": "TestComp2", "m": 2.0, "sigma": 3.5, "epsilon_k": 150.0}
        ]
        with open(DUMMY_PARAMS_FILEPATH, 'w') as f:
            json.dump(dummy_data_content, f, indent=2)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up resources after all tests in this class.
        Remove the dummy parameters file.
        """
        if os.path.exists(DUMMY_PARAMS_FILEPATH):
            os.remove(DUMMY_PARAMS_FILEPATH)
        # Attempt to remove directory if empty, fail silently if not.
        try:
            os.rmdir(TEST_DATA_DIR)
        except OSError:
            pass # Directory might not be empty if other files were created

    def test_initialization_success(self):
        """Test successful initialization with a valid parameters file."""
        characterizer = PetroleumCharacterization(initial_params_path=DUMMY_PARAMS_FILEPATH)
        self.assertIsNotNone(characterizer, "Characterizer should initialize.")
        self.assertIsNotNone(characterizer.ml_model, "ML model should be instantiated.")
        self.assertIsNone(characterizer.pcsaft_model, "PC-SAFT model should be None (placeholder).")
        self.assertEqual(len(characterizer.initial_pseudo_components), 2,
                         "Should load 2 components from dummy_params.json.")
        self.assertEqual(characterizer.initial_pseudo_components[0]["name"], "TestComp1")

    def test_initialization_file_not_found(self):
        """Test initialization with a non-existent parameters file."""
        # PetroleumCharacterization's _load_initial_parameters prints an error and returns []
        # We can check if initial_pseudo_components is empty or a default.
        characterizer = PetroleumCharacterization(initial_params_path=NON_EXISTENT_PARAMS_FILEPATH)
        self.assertIsNotNone(characterizer, "Characterizer should still initialize.")
        self.assertEqual(characterizer.initial_pseudo_components, [],
                         "initial_pseudo_components should be an empty list if file not found.")

    def test_initialization_default_path(self):
        """
        Test initialization using the default initial_params_path.
        This test is more of an integration test and depends on the default file existing.
        For true unit testing, explicit paths are better.
        We will assume the default file 'data/pseudo_components_initial.json' exists for this.
        """
        default_params_path = os.path.join(project_root, "data", "pseudo_components_initial.json")
        if not os.path.exists(default_params_path):
            self.skipTest(f"Default params file {default_params_path} not found, skipping test.")

        characterizer = PetroleumCharacterization(initial_params_path=None) # Uses default path
        self.assertIsNotNone(characterizer)
        self.assertTrue(len(characterizer.initial_pseudo_components) > 0,
                        "Should load components from the default data/pseudo_components_initial.json")


    def test_characterize_fluid_output_structure(self):
        """Test the return type and top-level keys of the characterize_fluid method."""
        characterizer = PetroleumCharacterization(initial_params_path=DUMMY_PARAMS_FILEPATH)
        sample_bulk_properties = {'API_gravity': 30, 'molecular_weight': 200}
        results = characterizer.characterize_fluid(bulk_properties=sample_bulk_properties)

        self.assertIsInstance(results, dict, "characterize_fluid should return a dictionary.")
        self.assertIn("bulk_inputs", results, "Results should contain 'bulk_inputs' key.")
        self.assertIn("adjusted_parameters", results, "Results should contain 'adjusted_parameters' key.")
        self.assertIn("pcsaft_outputs", results, "Results should contain 'pcsaft_outputs' key.")
        self.assertIn("notes", results, "Results should contain 'notes' key.")

        self.assertEqual(results["bulk_inputs"], sample_bulk_properties)

    def test_characterize_fluid_adjusted_parameters_structure(self):
        """Test the structure of 'adjusted_parameters' in the output of characterize_fluid."""
        characterizer = PetroleumCharacterization(initial_params_path=DUMMY_PARAMS_FILEPATH)
        sample_bulk_properties = {'API_gravity': 30, 'molecular_weight': 200}
        results = characterizer.characterize_fluid(bulk_properties=sample_bulk_properties)

        adjusted_params = results.get("adjusted_parameters")
        self.assertIsInstance(adjusted_params, list, "'adjusted_parameters' should be a list.")
        self.assertEqual(len(adjusted_params), 5,
                         "'adjusted_parameters' should contain 5 elements (from placeholder ML model).")

        for component_params in adjusted_params:
            self.assertIsInstance(component_params, dict, "Each component's parameters should be a dictionary.")
            self.assertIn("name", component_params)
            self.assertIn("m", component_params)
            self.assertIn("sigma", component_params)
            self.assertIn("epsilon_k", component_params)


if __name__ == '__main__':
    # This allows running the tests directly from this file
    unittest.main()
