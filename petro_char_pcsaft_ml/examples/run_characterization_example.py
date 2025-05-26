# examples/run_characterization_example.py

import os
import sys
import json # For printing dictionaries nicely
import matplotlib.pyplot as plt

# --- Path Adjustment ---
# Adjust the Python path to include the 'src' directory
# This allows the script to be run from the project root directory (e.g., petro_char_pcsaft_ml/)
# and correctly import modules from 'src'.
current_dir = os.path.dirname(os.path.abspath(__file__)) # examples directory
project_root = os.path.dirname(current_dir) # petro_char_pcsaft_ml directory
src_path = os.path.join(project_root, "src")
output_dir = os.path.join(current_dir, "outputs") # For saving plots

if src_path not in sys.path:
    sys.path.insert(0, src_path)

# --- Imports from src ---
# Now that sys.path is adjusted, we can import from src
try:
    from characterization import PetroleumCharacterization
    # ParameterAdjustmentModel is used within PetroleumCharacterization, direct import not essential here.
except ImportError as e:
    print(f"Error importing modules from 'src': {e}")
    print("Please ensure that the script is run from the project root directory 'petro_char_pcsaft_ml/',")
    print(f"and the 'src' directory with __init__.py, characterization.py, and ml_model.py exists at: {src_path}")
    sys.exit(1)

def main():
    """
    Main function to run the C7+ petroleum characterization example
    and generate plots of the results.
    """
    print("--- Starting C7+ Petroleum Characterization Example ---")

    # Create output directory for plots if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nPlots will be saved in: {os.path.abspath(output_dir)}")

    # 1. Define Sample Input Data - Whole Crude Properties
    # ----------------------------------------------------
    whole_crude_properties = {
        'API_gravity': 35.0,
        'gas_oil_ratio': 800.0,
        'c1_mole_fraction_overall': 0.30,
        'c2_mole_fraction_overall': 0.10,
        'c3_mole_fraction_overall': 0.05,
        'c4_mole_fraction_overall': 0.03,
        'c5_mole_fraction_overall': 0.02,
        'c6_mole_fraction_overall': 0.01,
    }
    print(f"\nStep 1: Defined Sample Input Properties for the Whole Crude Oil:")
    print(json.dumps(whole_crude_properties, indent=2))
    
    c7plus_mole_fraction_overall = 1.0 - (
        whole_crude_properties['c1_mole_fraction_overall'] +
        whole_crude_properties['c2_mole_fraction_overall'] +
        whole_crude_properties['c3_mole_fraction_overall'] +
        whole_crude_properties['c4_mole_fraction_overall'] +
        whole_crude_properties['c5_mole_fraction_overall'] +
        whole_crude_properties['c6_mole_fraction_overall']
    )
    print(f"  Implied C7+ mole fraction in whole crude: {c7plus_mole_fraction_overall:.4f}")

    # 2. Construct Paths
    # ------------------
    initial_params_filename = "pseudo_components_initial.json"
    initial_params_path = os.path.join(project_root, "data", initial_params_filename)
    print(f"\nStep 2: Constructed Paths:")
    print(f"  Path to initial C7+ pseudo-component parameters: {initial_params_path}")
    ml_model_file_path = None
    print(f"  Path to ML model file: {ml_model_file_path if ml_model_file_path else 'None (using placeholder model)'}")

    # 3. Instantiate PetroleumCharacterization
    # ----------------------------------------
    print("\nStep 3: Instantiating PetroleumCharacterization tool...")
    try:
        characterizer = PetroleumCharacterization(
            ml_model_path=ml_model_file_path,
            initial_params_path=initial_params_path
        )
        print("  PetroleumCharacterization tool instantiated successfully.")
    except FileNotFoundError as e:
        print(f"  Error during instantiation: {e}")
        return
    except Exception as e:
        print(f"  An unexpected error occurred during instantiation: {e}")
        return

    # 4. Call the C7+ Characterization Method
    # ---------------------------------------
    print("\nStep 4: Calling 'characterize_c7plus_fraction' method...")
    c7plus_results = characterizer.characterize_c7plus_fraction(
        bulk_properties_whole_fluid=whole_crude_properties
    )
    print("  'characterize_c7plus_fraction' method executed.")

    # 5. Display the Results for the C7+ Fraction
    # -------------------------------------------
    print("\n--- C7+ Fraction Characterization Results ---")
    print("\nInput Bulk Properties (Whole Crude):")
    print(json.dumps(c7plus_results.get('bulk_inputs_whole_fluid', {}), indent=2))

    predicted_c7plus_params = c7plus_results.get('predicted_c7plus_parameters', [])
    if predicted_c7plus_params:
        print("\nPredicted Parameters for the 5 C7+ Pseudo-components (describing the C7+ fraction):")
        component_names = []
        mole_fractions = []
        molar_masses = []
        calculated_sum_mole_fractions_c7plus = 0.0

        for i, params in enumerate(predicted_c7plus_params):
            name = params.get('name', f'Comp {i+1}')
            component_names.append(name)
            mf = params.get('mole_fraction', 0.0)
            mole_fractions.append(mf)
            molar_masses.append(params.get('molar_mass', 0.0))
            
            print(f"  Pseudo-component {i+1} ({name}):")
            print(f"    m (PC-SAFT)             : {params.get('m', 'N/A'):.2f}")
            print(f"    sigma (PC-SAFT)         : {params.get('sigma', 'N/A'):.2f} A")
            print(f"    epsilon_k (PC-SAFT)     : {params.get('epsilon_k', 'N/A'):.1f} K")
            print(f"    Mole Fraction (in C7+)  : {mf:.4f}")
            print(f"    Molar Mass              : {params.get('molar_mass', 'N/A'):.1f} g/mol")
            if isinstance(mf, (int, float)):
                calculated_sum_mole_fractions_c7plus += mf
        
        print(f"\n  Sum of predicted C7+ pseudo-component mole fractions: {calculated_sum_mole_fractions_c7plus:.4f}")
        if abs(calculated_sum_mole_fractions_c7plus - 1.0) > 1e-3:
            print("  Warning: The sum of mole fractions for C7+ pseudo-components does not equal 1.0.")

        # 6. Generate and Save Plots
        # --------------------------
        print("\nStep 6: Generating and saving plots...")

        # Mole Fraction Plot
        plt.figure(figsize=(10, 6))
        plt.bar(component_names, mole_fractions, color='skyblue')
        plt.title('Predicted Mole Fractions of C7+ Pseudo-components')
        plt.ylabel('Mole Fraction (within C7+ fraction)')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        mf_plot_path = os.path.join(output_dir, "c7plus_mole_fractions.png")
        plt.savefig(mf_plot_path)
        print(f"  Mole fraction plot saved to: {os.path.abspath(mf_plot_path)}")
        plt.close()

        # Molar Mass Plot
        plt.figure(figsize=(10, 6))
        plt.bar(component_names, molar_masses, color='lightcoral')
        plt.title('Predicted Molar Masses of C7+ Pseudo-components')
        plt.ylabel('Molar Mass (g/mol)')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        mm_plot_path = os.path.join(output_dir, "c7plus_molar_masses.png")
        plt.savefig(mm_plot_path)
        print(f"  Molar mass plot saved to: {os.path.abspath(mm_plot_path)}")
        plt.close()

    else:
        print("  No predicted parameters found for C7+ pseudo-components in results. Skipping plot generation.")

    print("\nPlaceholder PC-SAFT Outputs for the C7+ Fraction:")
    pcsaft_outputs_c7plus = c7plus_results.get('pcsaft_outputs_c7plus', {})
    if pcsaft_outputs_c7plus:
        print(json.dumps(pcsaft_outputs_c7plus, indent=2))
    else:
        print("  No PC-SAFT outputs for C7+ fraction found in results.")

    print(f"\nNotes from Characterization: {c7plus_results.get('notes', 'N/A')}")
    print("\n--- End of C7+ Petroleum Characterization Example ---")

if __name__ == "__main__":
    main()
