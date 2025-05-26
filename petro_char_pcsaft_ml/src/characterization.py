"""
Core Petroleum Fluid Characterization Logic for C7+ Fraction.

This module defines the `PetroleumCharacterization` class, which orchestrates
the process of characterizing the C7+ (heptanes and heavier) fraction of a
petroleum fluid. It integrates predictions from a machine learning model
(for PC-SAFT parameters, mole fractions, and molar masses of C7+ pseudo-components)
with (placeholder) PC-SAFT calculations to estimate fluid properties.
"""

import json
import os
from .ml_model import ParameterAdjustmentModel
# from sgtpy import component, saft # Example for future PC-SAFT library integration

class PetroleumCharacterization:
    """
    Manages the C7+ petroleum fluid characterization process.

    This class integrates Machine Learning (ML) predictions for PC-SAFT
    (Perturbed-Chain Statistical Associating Fluid Theory) pseudo-component
    parameters, mole fractions, and molar masses, with subsequent (placeholder)
    PC-SAFT calculations focused on the C7+ fraction.

    Attributes:
        initial_params_path (str): Path to the JSON file containing initial
                                   parameters for C7+ pseudo-components.
        initial_pseudo_components (list): A list of dictionaries, where each
                                          dictionary holds the initial parameters
                                          (including m, sigma, epsilon_k,
                                          mole_fraction, molar_mass) for a C7+
                                          pseudo-component, loaded from
                                          `initial_params_path`.
        ml_model (ParameterAdjustmentModel): An instance of the ML model used for
                                             predicting/adjusting C7+ pseudo-component
                                             parameters.
        pcsaft_model (any): Placeholder for an actual PC-SAFT model instance or
                            library interface. Currently `None`.
    """

    def __init__(self, ml_model_path=None, initial_params_path=None):
        """
        Initializes the PetroleumCharacterization tool for C7+ fractions.

        This involves loading initial C7+ pseudo-component parameters (including
        PC-SAFT params, mole fractions, and molar masses) from a JSON file and
        instantiating the ML model. A placeholder for the PC-SAFT model is also
        initialized.

        Args:
            ml_model_path (str, optional): Path to a trained ML model file for
                                           the `ParameterAdjustmentModel`.
                                           Defaults to None (placeholder model behavior).
            initial_params_path (str, optional): Path to the JSON file containing
                                                 initial parameters for C7+
                                                 pseudo-components. If None, it
                                                 defaults to a path relative to this
                                                 project: `data/pseudo_components_initial.json`.
        """
        print("Initializing PetroleumCharacterization for C7+ fraction...")

        if initial_params_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Project root
            self.initial_params_path = os.path.join(base_dir, "data", "pseudo_components_initial.json")
        else:
            self.initial_params_path = initial_params_path

        self.initial_pseudo_components = self._load_initial_parameters()

        self.ml_model = ParameterAdjustmentModel(model_path=ml_model_path)
        print(f"ParameterAdjustmentModel instantiated (model path: {ml_model_path if ml_model_path else 'None - placeholder model used'}).")

        self.pcsaft_model = None
        print("Placeholder: PC-SAFT model would be initialized here (currently set to None).")

        if self.initial_pseudo_components:
             print(f"Successfully loaded {len(self.initial_pseudo_components)} initial C7+ pseudo-components from: {self.initial_params_path}")
        else:
             print(f"Warning/Info: No initial C7+ pseudo-components loaded from: {self.initial_params_path}.")


    def _load_initial_parameters(self):
        """
        Loads initial parameters for C7+ pseudo-components from a JSON file.

        These parameters include name, m, sigma, epsilon_k, mole_fraction,
        and molar_mass for each C7+ pseudo-component.

        Returns:
            list[dict]: A list of dictionaries, each representing a C7+
                        pseudo-component with its parameters. Returns an
                        empty list if loading fails.
        """
        try:
            with open(self.initial_params_path, 'r') as f:
                params = json.load(f)
            return params
        except FileNotFoundError:
            print(f"Error: Initial C7+ parameters file not found at {self.initial_params_path}")
            return []
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.initial_params_path}. Check file format.")
            return []


    def characterize_c7plus_fraction(self, bulk_properties_whole_fluid):
        """
        Characterizes the C7+ fraction of a petroleum fluid based on bulk properties.

        The process involves:
        1. Using the ML model (`self.ml_model`) to predict PC-SAFT parameters,
           mole fractions, and molar masses for a set of C7+ pseudo-components,
           based on the `bulk_properties_whole_fluid`.
        2. (Placeholder) Using these predicted parameters for the C7+ fraction
           with a PC-SAFT model to calculate various fluid properties of this fraction.

        Args:
            bulk_properties_whole_fluid (dict): A dictionary of bulk fluid properties
                                    for the entire petroleum fluid (including C1-C6 if any).
                                    Example: `{'API_gravity': 35, 'overall_molecular_weight': 150}`.
                                    The keys should match what `self.ml_model.predict` expects.

        Returns:
            dict: A dictionary containing the characterization results for the C7+ fraction.
                  This includes:
                  - 'bulk_inputs_whole_fluid': The original `bulk_properties_whole_fluid`.
                  - 'predicted_c7plus_parameters': A list of dictionaries, where each
                                                   dictionary contains the 'name', 'm', 'sigma',
                                                   'epsilon_k', 'mole_fraction', and 'molar_mass'
                                                   for one C7+ pseudo-component.
                  - 'pcsaft_outputs_c7plus': A dictionary of (currently placeholder)
                                             fluid properties calculated by PC-SAFT for
                                             the C7+ fraction.
                  - 'notes': A string with relevant notes.
        """
        print(f"\nStarting C7+ fraction characterization based on whole fluid properties: {bulk_properties_whole_fluid}")

        # 1. Use the ML model to get parameters for C7+ pseudo-components
        # The ML model is assumed to predict parameters for the C7+ fraction
        # based on properties of the whole crude.
        predicted_c7plus_parameters = self.ml_model.predict(bulk_properties_whole_fluid)
        
        print("\nML Model Predicted Parameters for C7+ Pseudo-components:")
        if predicted_c7plus_parameters:
            total_mole_fraction_c7plus = 0.0
            for i, params in enumerate(predicted_c7plus_parameters):
                print(f"  Pseudo-component {i+1} ({params.get('name', 'N/A')}): "
                      f"m={params.get('m')}, sigma={params.get('sigma')}, "
                      f"epsilon_k={params.get('epsilon_k')}, "
                      f"mole_fraction={params.get('mole_fraction')}, "
                      f"molar_mass={params.get('molar_mass')}")
                if isinstance(params.get('mole_fraction'), (int, float)):
                    total_mole_fraction_c7plus += params.get('mole_fraction')
            print(f"  Sum of predicted C7+ mole fractions: {total_mole_fraction_c7plus:.4f}")
            if abs(total_mole_fraction_c7plus - 1.0) > 1e-3: # Allow for small numerical inaccuracies
                 print("  Warning: Sum of predicted C7+ mole fractions is not 1.0. This might need normalization depending on the model's behavior.")
        else:
            print("  ML model did not return any parameters for C7+ pseudo-components.")

        # 2. (Placeholder) Use the predicted C7+ parameters with the PC-SAFT model
        print("\nPlaceholder: PC-SAFT Calculation Step for C7+ Fraction")
        print("  This step would use the 'predicted_c7plus_parameters' (including their")
        print("  PC-SAFT params m, sigma, epsilon_k, mole fractions, and molar masses)")
        print("  with a PC-SAFT library to model the thermodynamic properties of the C7+ fraction.")
        print("  To model the whole crude, parameters for C1-C6 components and their overall proportions")
        print("  relative to the C7+ fraction would also be needed.")
        
        pcsaft_outputs_c7plus = {
            "density_c7plus_kg_m3": "Placeholder (e.g., 780 kg/m^3 for C7+ fraction)",
            "viscosity_c7plus_cP": "Placeholder (e.g., 2.5 cP for C7+ fraction)",
            "notes_pcsaft": "These are placeholder values for the C7+ fraction properties."
        }
        print(f"  Placeholder PC-SAFT outputs for C7+ fraction generated: {pcsaft_outputs_c7plus}")

        results = {
            "bulk_inputs_whole_fluid": bulk_properties_whole_fluid,
            "predicted_c7plus_parameters": predicted_c7plus_parameters,
            "pcsaft_outputs_c7plus": pcsaft_outputs_c7plus,
            "notes": "This result focuses on the C7+ fraction characterization. "
                     "True ML predictions and PC-SAFT calculations are not yet implemented."
        }

        print("\nC7+ fraction characterization process complete (using placeholders).")
        return results

if __name__ == '__main__':
    print("\n--- Example Usage of PetroleumCharacterization for C7+ Fraction ---")

    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    # Using the C7+ focused initial parameters file by default now
    initial_params_file = os.path.join(project_root, "data", "pseudo_components_initial.json")
    
    if not os.path.exists(initial_params_file):
        print(f"\nWarning for __main__ example: Default initial_params_file not found at {initial_params_file}")
        initial_params_file_for_init = None # Pass None to use class's default logic or handle error
    else:
        initial_params_file_for_init = initial_params_file
        
    # 1. Initialize the characterization tool
    try:
        characterizer = PetroleumCharacterization(
            ml_model_path=None, # Uses placeholder ML model
            initial_params_path=initial_params_file_for_init
        )
    except Exception as e:
        print(f"Error during PetroleumCharacterization instantiation in __main__: {e}")
        characterizer = None

    if characterizer:
        # 2. Define sample bulk properties for the *whole* petroleum fluid
        sample_whole_fluid_properties = {
            'API_gravity': 38.0,                # For the whole fluid
            'overall_molecular_weight': 160.0,  # For the whole fluid (g/mol)
            'T50_boiling_point': 280.0          # For the whole fluid (degrees C)
        }
        print(f"\nInput Bulk Properties for the Whole Fluid: {json.dumps(sample_whole_fluid_properties, indent=2)}")

        # 3. Run the C7+ characterization
        # The method now explicitly states it characterizes the C7+ fraction
        c7plus_characterization_results = characterizer.characterize_c7plus_fraction(
            bulk_properties_whole_fluid=sample_whole_fluid_properties
        )

        # 4. Print the results for the C7+ fraction
        print("\n--- C7+ Fraction Characterization Results ---")
        print(f"Original Bulk Inputs (Whole Fluid): {json.dumps(c7plus_characterization_results.get('bulk_inputs_whole_fluid'), indent=2)}")
        
        print("\nPredicted Parameters for C7+ Pseudo-components:")
        predicted_params = c7plus_characterization_results.get('predicted_c7plus_parameters', [])
        if predicted_params:
            total_mole_fraction = 0
            for i, params in enumerate(predicted_params):
                print(f"  Component {i+1} ({params.get('name', 'N/A')}):")
                print(f"    m             = {params.get('m', 'N/A'):.2f}")
                print(f"    sigma         = {params.get('sigma', 'N/A'):.2f} A")
                print(f"    epsilon_k     = {params.get('epsilon_k', 'N/A'):.1f} K")
                print(f"    mole_fraction = {params.get('mole_fraction', 'N/A'):.4f} (within C7+ fraction)")
                print(f"    molar_mass    = {params.get('molar_mass', 'N/A'):.1f} g/mol")
                if isinstance(params.get('mole_fraction'), (int, float)):
                    total_mole_fraction += params.get('mole_fraction', 0)
            print(f"  Sum of C7+ component mole fractions: {total_mole_fraction:.4f}")
        else:
            print("  No predicted parameters for C7+ components found.")
            
        print(f"\nPC-SAFT Outputs (Placeholder for C7+ Fraction): {json.dumps(c7plus_characterization_results.get('pcsaft_outputs_c7plus'), indent=2)}")
        print(f"\nNotes: {c7plus_characterization_results.get('notes')}")
    else:
        print("\nPetroleumCharacterization tool could not be initialized. Example usage aborted.")

    print("\n--- End of Example Usage ---")
