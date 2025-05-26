# PetroChar PCSAFT ML

## Purpose

This project aims to develop a tool for petroleum fluid characterization, with a specific focus on the C7+ (heptanes and heavier) fraction. It uses a combination of Machine Learning (ML) techniques and the Perturbed-Chain Statistical Associating Fluid Theory (PC-SAFT) equation of state.

The core idea is to:
1.  Use an ML model to predict key parameters (PC-SAFT parameters, mole fractions, and molar masses) for a set of pseudo-components representing the C7+ fraction. This prediction is based on readily available bulk experimental data of the *whole crude oil*.
2.  Employ these ML-derived parameters for the C7+ pseudo-components within a PC-SAFT framework to model their thermodynamic and transport properties.
3.  (Future) Integrate these C7+ pseudo-components with known parameters for lighter components (C1-C6) to model the entire fluid.
4.  (Future) Optimize the pseudo-component parameters by fitting them to experimental fluid property data.

This approach seeks to provide a more accurate and efficient characterization workflow for the complex C7+ fraction, which is crucial for overall fluid behavior modeling.

## Background Concepts

### Petroleum Fluid Characterization

Petroleum fluids (crude oils, condensates, natural gases) are extraordinarily complex mixtures. While lighter components (C1-C6, i.e., methane to hexanes) can often be identified and their properties are well-known, the **C7+ fraction** (heptanes and heavier components) consists of thousands of different hydrocarbon compounds. Directly modeling each compound in the C7+ fraction is computationally infeasible.

**Petroleum fluid characterization** is the process of simplifying this complex C7+ mixture into a manageable number of "pseudo-components." Each pseudo-component represents a group of hydrocarbons within the C7+ fraction that have similar average properties. The goal is to determine the properties of these pseudo-components—such as their average molecular weight, PC-SAFT parameters, and their respective mole fractions within the C7+ mixture—so that the behavior of the C7+ fraction, and subsequently the entire fluid, can be accurately modeled.

**This project specifically focuses on characterizing the C7+ fraction of a petroleum fluid into five pseudo-components.**

### PC-SAFT Equation of State

The **Perturbed-Chain Statistical Associating Fluid Theory (PC-SAFT)** is an advanced equation of state (EoS) used to calculate the thermodynamic properties of pure fluids and mixtures. It is particularly well-suited for complex fluids, including polymers and, relevant to this project, petroleum fluids and their C7+ fractions.

PC-SAFT models molecules as chains of spherical segments. The model accounts for:
*   **Repulsive forces** between segments (hard-chain reference term, `Z_hc`).
*   **Attractive forces** (dispersion forces) between segments (dispersion term, `Z_disp`).
*   **Association effects** (e.g., hydrogen bonding) if present (association term, `Z_assoc`), though this term is often less critical for non-associating hydrocarbon systems typically found in C7+ fractions.

For each pure component or pseudo-component, PC-SAFT typically requires three main parameters:
*   `m`: The number of spherical segments per chain molecule (related to molecular size).
*   `sigma` (σ): The diameter of each segment (Angstroms).
*   `epsilon/k` (ε/k): The energy parameter, representing the depth of the potential well between non-bonded segments (Kelvin).

The compressibility factor `Z` (which relates pressure, volume, and temperature: `Z = PV/nRT`) is generally expressed as a sum of contributions:
`Z = 1 + Z_hc + Z_disp (+ Z_assoc for associating fluids)`

By calculating `Z` and its derivatives, various thermodynamic properties such as density, enthalpy, entropy, phase equilibria (vapor-liquid, liquid-liquid), and critical points can be determined.

## Machine Learning for Enhanced Characterization

The accuracy of PC-SAFT (and any EoS) in predicting fluid properties heavily relies on the quality of the input parameters (`m`, `sigma`, `epsilon_k`), molar masses, and mole fractions for each pseudo-component, especially for the C7+ fraction. Determining these for pseudo-components that best represent the C7+ mixture is a significant challenge.

This project proposes to leverage Machine Learning (ML) to estimate these parameters for the C7+ pseudo-components.

### Proposed ML Workflow

The envisioned workflow for ML integration is as follows:

1.  **Inputs to the ML Model**:
    The ML model is designed to take readily available, measurable bulk properties of the **whole crude oil** as input. Examples include:
    *   API gravity of the whole crude
    *   Gas-Oil Ratio (GOR)
    *   Mole fractions of light ends (C1-C6) in the whole crude
    *   Overall fluid viscosity or density (at specific conditions)
    *   Distillation curve data (e.g., T10, T50, T90 boiling points) for the whole crude

2.  **ML Model Type**:
    A supervised learning approach, specifically a regression model, is envisioned. The current implementation in `src/ml_model.py` (`ParameterAdjustmentModel`) is a **placeholder**. It does not contain a trained model or the logic for training one but illustrates the I/O structure.

3.  **Outputs from the ML Model**:
    The ML model's primary output is a detailed characterization of the **five C7+ pseudo-components**. For each of these five pseudo-components, the model predicts:
    *   `m` (PC-SAFT number of segments)
    *   `sigma` (PC-SAFT segment diameter)
    *   `epsilon_k` (PC-SAFT energy parameter)
    *   `mole_fraction`: The mole fraction of the pseudo-component **within the C7+ fraction itself**. The sum of these mole fractions for the 5 C7+ pseudo-components must equal 1.0.
    *   `molar_mass`: The average molar mass of the pseudo-component.

### Benefit of ML Integration

By training an ML model on a dataset of known petroleum fluids (where bulk properties of the whole crude are linked to "optimal" C7+ pseudo-component parameters that accurately reproduce experimental data), the model can learn complex relationships. This approach aims to provide a more robust and data-driven method for characterizing the C7+ fraction compared to traditional generalized correlations.

### Conceptual Flow Diagram (C7+ Focus)

The overall process for characterizing the C7+ fraction can be visualized as:

```
Input Bulk Properties of Whole Crude Oil (e.g., API, GOR, C1-C6 content)
                      │
                      ▼
[Machine Learning Model (src/ml_model.py - Placeholder)]
  (Predicts parameters for 5 C7+ pseudo-components)
                      │
                      ▼
Detailed C7+ Pseudo-component Parameters:
  - PC-SAFT params (m, sigma, epsilon_k)
  - Mole Fractions (within C7+, sum to 1.0)
  - Molar Masses
                      │
                      ▼
[PC-SAFT Equation of State (src/pcsaft_wrapper.py - Placeholder)]
  (Calculates properties of the C7+ fraction using predicted parameters)
                      │
                      ▼
Calculated Properties of the C7+ Fraction (e.g., Density, Viscosity)
```
(Further steps would involve combining this C7+ characterization with C1-C6 data to model the whole fluid.)

## Current Project Stage

The project, in its current form, provides the **foundational software framework and workflow orchestration** for the described C7+ petroleum characterization method. It establishes the conceptual structure and demonstrates the intended flow of data and calculations for the C7+ fraction, but does not yet include fully implemented scientific computations.

This framework includes:
*   A **well-defined directory structure**.
*   **Placeholder modules** for key scientific components:
    *   PC-SAFT calculations (`src/pcsaft_wrapper.py`).
    *   Machine Learning model (`src/ml_model.py`), now geared to output detailed C7+ parameters.
*   The **core characterization logic** (`src/characterization.py`): Implements `PetroleumCharacterization` with its `characterize_c7plus_fraction` method, demonstrating how whole crude properties feed into the (placeholder) ML model to yield detailed C7+ pseudo-component parameters.
*   **Example data structures**:
    *   Initial parameters for C7+ pseudo-components (`data/pseudo_components_initial.json`), including mole fractions and molar masses.
    *   A conceptual layout for ML training data (`data/training_data_placeholder.csv`) reflecting the expanded C7+ outputs.
*   An **example script** (`examples/run_characterization_example.py`) that allows users to run the C7+ placeholder workflow and see the conceptual data flow and outputs.
*   **Unit tests** (`tests/test_characterization.py`) verifying the C7+ focused logic.

**Emphasis on Future Work**: The detailed implementation of the PC-SAFT equations and the development, training, and validation of the ML model for C7+ characterization are significant **areas for future development**.

## Hypothetical Results / Expected Outcome

Since the Machine Learning model within this project is currently a placeholder (not trained) and the PC-SAFT calculations are not yet fully integrated, this section describes the **anticipated outcomes** and the **kind of results** the project aims to produce once fully developed.

### ML Model Output and Visualization

A successfully trained ML model would, given bulk properties of a whole crude oil, output a detailed characterization of its C7+ fraction. This characterization would comprise:
*   **PC-SAFT parameters** (`m`, `sigma`, `epsilon_k`) for each of the five C7+ pseudo-components.
*   The **mole fraction** of each pseudo-component within the C7+ fraction (these five mole fractions would sum to 1.0).
*   The average **molar mass** for each pseudo-component.

The `examples/run_characterization_example.py` script, even with the current placeholder ML model, demonstrates the *structure* of this output. Running this script (`python examples/run_characterization_example.py` from the project root) will generate illustrative plots:
*   `examples/outputs/c7plus_mole_fractions.png`: A bar chart showing the distribution of mole fractions among the five C7+ pseudo-components.
*   `examples/outputs/c7plus_molar_masses.png`: A bar chart showing the molar mass for each C7+ pseudo-component.
These plots visually represent the type of detailed C7+ breakdown this project aims for, providing a clear picture of the C7+ fraction's composition as predicted by the (future) ML model.

### Application in PC-SAFT for Fluid Property Prediction

The detailed parameters for the C7+ pseudo-components, derived from the ML model, are crucial inputs for the PC-SAFT equation of state. The intended application is:
1.  The five C7+ pseudo-components, now characterized with their specific PC-SAFT parameters, mole fractions, and molar masses, would be defined within a PC-SAFT modeling environment.
2.  These C7+ pseudo-components would then be combined with known parameters for the lighter components (C1-C6) of the petroleum fluid, using their respective overall mole fractions in the total mixture.
3.  The PC-SAFT EoS would then be used to calculate various thermodynamic and transport properties of the **entire petroleum fluid**. Examples include:
    *   Density and viscosity at various temperatures and pressures.
    *   Phase envelopes (P-T, T-x/y diagrams).
    *   Saturation pressures (bubble point, dew point).
    *   Flash calculations.

### Validation and Overall Benefit

The ultimate success of this ML-enhanced characterization approach would be validated by comparing the PC-SAFT-predicted properties (using the ML-derived C7+ parameters) against experimental data for the specific crude oil being analyzed. A well-trained ML model is expected to yield C7+ parameters that allow PC-SAFT to more accurately match these experimental measurements.

The **expected outcome** is a more accurate, data-driven, and potentially more efficient method for characterizing the C7+ fraction of petroleum fluids. This, in turn, leads to more reliable thermodynamic modeling, which is essential for various petroleum engineering applications, such as reservoir simulation, flow assurance, and process design.

## Conceptual Conclusions / Future Outlook

This project successfully establishes a **foundational software framework** and a **clear workflow** for a C7+ petroleum fluid characterization process. It demonstrates how machine learning can be conceptually integrated to predict detailed parameters (PC-SAFT parameters, mole fractions, molar masses) for C7+ pseudo-components based on whole crude oil properties. The current structure includes essential components like data handling conventions, placeholder modules for ML prediction and PC-SAFT calculations, a core characterization orchestration class, and an example script with visualizations that illustrates the intended data flow and outputs.

The **potential of this approach** lies in its ability to provide a more detailed and data-driven characterization of the complex C7+ fraction compared to traditional methods that often rely on generalized correlations. This can lead to improved accuracy in thermodynamic modeling of petroleum fluids using equations of state like PC-SAFT.

To realize the full potential of this project, the following **key next steps** are critical:

1.  **PC-SAFT Integration**:
    *   Implement actual PC-SAFT calculations within `src/pcsaft_wrapper.py`. This will involve selecting and integrating a suitable PC-SAFT library (e.g., `sgtpy`, which is already listed in `requirements.txt`) or developing a custom PC-SAFT implementation.
    *   Connect this implementation to the `PetroleumCharacterization` workflow so it can use the ML-derived C7+ pseudo-component parameters (including their mole fractions and molar masses) to calculate thermodynamic properties of the C7+ fraction.

2.  **Machine Learning Model Development**:
    *   **Data Acquisition/Generation**: This is a crucial and often challenging step, requiring a robust dataset that links bulk properties of various whole crude oils to corresponding "true" or well-validated C7+ pseudo-component parameters (PC-SAFT parameters, mole fractions, and molar masses). This may require extensive laboratory analysis of crude oils and/or detailed compositional simulations to generate reliable target data.
    *   **Model Selection and Training**: Choose an appropriate supervised regression model (e.g., gradient boosting, random forests, neural networks). Train this model using the acquired dataset to predict the five sets of C7+ pseudo-component parameters from whole crude properties.
    *   **Model Integration**: Replace the current placeholder `ParameterAdjustmentModel` in `src/ml_model.py` with the fully trained and validated ML model.

3.  **Validation and Refinement**:
    *   Rigorously validate the entire integrated system. This involves comparing the thermodynamic properties predicted by the PC-SAFT model (using ML-derived C7+ parameters and combined with C1-C6 data) against comprehensive experimental data for a diverse range of crude oils.
    *   Refine the ML model and characterization workflow based on validation results.

4.  **(Optional) Further Expansions**:
    *   **Integration of C1-C6 Components**: Develop a more seamless workflow for combining the characterized C7+ fraction with light end (C1-C6) data to model the entire fluid.
    *   **Uncertainty Quantification**: Incorporate methods to quantify the uncertainty in the ML predictions and its impact on the final fluid property calculations.
    *   **Optimization**: Explore optimization routines for fine-tuning pseudo-component definitions or parameters based on specific experimental targets.

By addressing these future development areas, this project can evolve from a conceptual framework into a powerful tool for petroleum fluid characterization, offering significant improvements in accuracy and efficiency for the petroleum industry.

## Project Structure

The project is organized as follows:
```
petro_char_pcsaft_ml/
├── .gitignore
├── README.md
├── data/
│   ├── pseudo_components_initial.json  # Initial parameters for 5 C7+ pseudo-components
│   └── training_data_placeholder.csv # Placeholder CSV for ML training (C7+ outputs)
├── docs/
│   └── .gitkeep
├── examples/
│   ├── run_characterization_example.py # Demonstrates C7+ characterization
│   └── outputs/                    # Directory for saved plots from example
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── characterization.py           # Core C7+ characterization workflow
│   ├── ml_model.py                   # Placeholder ML model for C7+ parameters
│   └── pcsaft_wrapper.py
└── tests/
    ├── __init__.py
    ├── test_characterization.py      # Tests for C7+ characterization
    └── test_data/
        ├── __init__.py
        └── dummy_params.json
```

## Setup Instructions

To set up the project locally, follow these steps:
1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd petro_char_pcsaft_ml
    ```
    (Replace `<repository_url>` with the actual URL of the repository.)
2.  **Create and activate a virtual environment** (recommended, Python 3.8+):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate  # On Windows
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The primary way to see the (current placeholder) C7+ characterization workflow is by running the example script.

1.  **Run the example script**:
    Ensure you are in the project root directory (`petro_char_pcsaft_ml/`) and your virtual environment is activated.
    ```bash
    python examples/run_characterization_example.py
    ```
    This will also generate plots in the `examples/outputs/` directory.

2.  **What the example does**:
    The `run_characterization_example.py` script demonstrates the C7+ focused workflow:
    *   It initializes the `PetroleumCharacterization` tool.
    *   It uses sample bulk properties of a **whole crude oil** (including light end mole fractions).
    *   It calls the `characterize_c7plus_fraction` method, which internally uses the placeholder `ParameterAdjustmentModel` to generate parameters (PC-SAFT params, mole fractions, molar masses) for **five C7+ pseudo-components**.
    *   It prints the input whole crude properties and then the detailed (currently dummy) parameters for the C7+ pseudo-components, including their mole fractions within the C7+ fraction and their molar masses.
    *   It generates and saves bar charts for the C7+ pseudo-component mole fractions and molar masses to the `examples/outputs/` directory.

## Running Tests

Unit tests verify the functionality of the placeholder components and workflow.
From the project root directory (`petro_char_pcsaft_ml/`):
```bash
python -m unittest discover -s tests
```

## Key Components

*   `src/characterization.py`: Contains `PetroleumCharacterization` with its `characterize_c7plus_fraction` method, which orchestrates the C7+ characterization workflow using whole crude properties as input.
*   `src/ml_model.py`: Defines `ParameterAdjustmentModel`, a **placeholder** that returns fixed dummy PC-SAFT parameters, mole fractions (summing to 1 for C7+), and molar masses for the five C7+ pseudo-components.
*   `src/pcsaft_wrapper.py`: A **placeholder** with dummy functions (returning fixed values) intended for PC-SAFT calculations.
*   `data/pseudo_components_initial.json`: Stores initial parameters for the five C7+ pseudo-components, including their names, PC-SAFT params, mole fractions (within C7+), and molar masses.
*   `data/training_data_placeholder.csv`: Shows the expected CSV format for ML training data, where inputs are whole crude properties and outputs are the detailed parameters for the C7+ pseudo-components.
*   `examples/run_characterization_example.py`: Demonstrates the C7+ characterization workflow using sample whole crude properties and saves output plots.
*   `examples/outputs/`: Directory where plots generated by the example script are saved.

## Future Work / Placeholders

This project is currently a scaffold for C7+ characterization. Key future work includes:
*   **Machine Learning Model (`src/ml_model.py`)**: Develop and train an actual ML model to predict C7+ pseudo-component parameters from whole crude data.
*   **PC-SAFT Integration (`src/pcsaft_wrapper.py`, `src/characterization.py`)**: Implement actual PC-SAFT calculations to determine properties of the C7+ fraction, and eventually the whole fluid by integrating C1-C6 data.
*   **Data Expansion**: Gather comprehensive datasets for ML model training and validation.

## Contributing
(Placeholder for contribution guidelines.)

## License
(Placeholder for license information.)
