# examples/run_characterization_example.py

import os
import sys
import json # For printing dictionaries nicely

# --- Path Adjustment ---
# Adjust the Python path to include the 'src' directory
# This allows the script to be run from the project root directory (e.g., petro_char_pcsaft_ml/)
# and correctly import modules from 'src'.
# Assumes this script is in 'petro_char_pcsaft_ml/examples/'
# and 'src' is in 'petro_char_pcsaft_ml/src/'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)

# --- Imports from src ---
# Now that sys.path is adjusted, we can import from src
try:
    from characterization import PetroleumCharacterization
    from ml_model import ParameterAdjustmentModel # Though not directly used, good to show it's importable
except ImportError as e:
    print(f"Error importing modules from 'src': {e}")
    print("Please ensure that the script is run from the project root directory 'petro_char_pcsaft_ml/',")
    print(f"and the 'src' directory with __init__.py, characterization.py, and ml_model.py exists at: {src_path}")
    sys.exit(1)

def main():
    """
    Main function to run the petroleum characterization example.
    """
    print("--- Starting Petroleum Characterization Example ---")

    # 1. Define Sample Input Data
    # ---------------------------
    # These are the bulk properties of the petroleum fluid that we want to characterize.
    # The keys used here (e.g., 'API_gravity') should match what the ML model
    # (ParameterAdjustmentModel.predict method) expects as input_features.
    bulk_petroleum_properties = {
        'API_gravity': 30.0,        # Example: API gravity of the fluid
        'molecular_weight': 200.5,  # Example: Average molecular weight (g/mol)
        'boiling_point_T50': 350.0  # Example: T50 boiling point (degrees Celsius)
    }
    print(f"\nStep 1: Defined Sample Bulk Petroleum Properties:")
    print(json.dumps(bulk_petroleum_properties, indent=2))

    # Mole fractions for the (e.g., 5) pseudo-components that will represent the fluid.
    # These must sum to 1.0. In a real application, these might also be
    # an output of the ML model or an optimization process.
    pseudo_component_mole_fractions = [0.10, 0.20, 0.30, 0.25, 0.15] # Sums to 1.0
    if not abs(sum(pseudo_component_mole_fractions) - 1.0) < 1e-9: # Check if sum is close to 1.0
        print("\nError: Pseudo-component mole fractions do not sum to 1.0.")
        return
    print(f"\nStep 2: Defined Sample Pseudo-component Mole Fractions:")
    print(pseudo_component_mole_fractions)

    # 2. Construct Paths
    # ------------------
    # Path to the file containing initial PC-SAFT parameters for pseudo-components.
    # This path is relative to the project root.
    initial_params_filename = "pseudo_components_initial.json"
    initial_params_path = os.path.join(project_root, "data", initial_params_filename)

    print(f"\nStep 3: Constructed Paths:")
    print(f"  Path to initial pseudo-component parameters: {initial_params_path}")

    # (Optional) Path to a pre-trained ML model file.
    # The current ParameterAdjustmentModel is a placeholder and doesn't load a file,
    # so `None` is acceptable for `ml_model_path`.
    ml_model_file_path = None # Or "path/to/your/trained_model.pkl" if you have one
    print(f"  Path to ML model file: {ml_model_file_path if ml_model_file_path else 'None (using placeholder model)'}")


    # 3. Instantiate PetroleumCharacterization
    # ----------------------------------------
    print("\nStep 4: Instantiating PetroleumCharacterization tool...")
    try:
        characterizer = PetroleumCharacterization(
            ml_model_path=ml_model_file_path,
            initial_params_path=initial_params_path
        )
        print("  PetroleumCharacterization tool instantiated successfully.")
    except FileNotFoundError as e:
        print(f"  Error during instantiation: {e}")
        print("  Please ensure the initial parameters JSON file exists at the specified path.")
        return
    except Exception as e:
        print(f"  An unexpected error occurred during instantiation: {e}")
        return

    # 4. Call the characterize_fluid method
    # -------------------------------------
    print("\nStep 5: Calling characterize_fluid method...")
    # Pass the bulk properties and mole fractions to the characterization tool.
    characterization_results = characterizer.characterize_fluid(
        bulk_properties=bulk_petroleum_properties,
        mole_fractions=pseudo_component_mole_fractions
    )
    print("  characterize_fluid method executed.")

    # 5. Print the Results
    # --------------------
    print("\n--- Characterization Results ---")

    print("\nInput Bulk Properties:")
    print(json.dumps(characterization_results.get('bulk_inputs', {}), indent=2))

    print("\nAdjusted Pseudo-component Parameters (from ML Model - Placeholder):")
    adjusted_params = characterization_results.get('adjusted_parameters', [])
    if adjusted_params:
        for i, params in enumerate(adjusted_params):
            name = params.get('name', f'Comp {i+1}')
            m = params.get('m', 'N/A')
            sigma = params.get('sigma', 'N/A')
            epsilon_k = params.get('epsilon_k', 'N/A')
            print(f"  {name}: m={m}, sigma={sigma} A, epsilon_k={epsilon_k} K")
    else:
        print("  No adjusted parameters found in results.")

    print("\nPlaceholder for PC-SAFT Results:")
    pcsaft_outputs = characterization_results.get('pcsaft_outputs', {})
    if pcsaft_outputs:
        print(json.dumps(pcsaft_outputs, indent=2))
    else:
        print("  No PC-SAFT outputs found in results.")

    print(f"\nNotes: {characterization_results.get('notes', 'N/A')}")
    print("\n--- End of Petroleum Characterization Example ---")

if __name__ == "__main__":
    main()
