# PetroChar PCSAFT ML

## Purpose

This project aims to develop a tool for petroleum fluid characterization using a combination of Machine Learning (ML) techniques and the Perturbed-Chain Statistical Associating Fluid Theory (PC-SAFT) equation of state.

The core idea is to:
1.  Use ML models to predict/adjust key parameters of pseudo-components based on readily available experimental data (e.g., API gravity, molecular weight, boiling points).
2.  Employ these ML-derived parameters within a PC-SAFT framework to model thermodynamic and transport properties of petroleum fluids.
3.  (Future) Optimize the pseudo-component parameters by fitting them to experimental fluid property data.

This approach seeks to provide a more accurate and efficient characterization workflow compared to traditional methods.

## Background Concepts

### Petroleum Fluid Characterization

Petroleum fluids (crude oils, condensates, natural gases) are extraordinarily complex mixtures, often containing thousands of different hydrocarbon compounds, along with non-hydrocarbon components. Directly modeling each compound is computationally infeasible for most engineering applications.

**Petroleum fluid characterization** is the process of simplifying this complex mixture into a manageable number of "pseudo-components" (or fractions). Each pseudo-component represents a group of hydrocarbons with similar properties. The goal is to determine the properties of these pseudo-components—such as their average molecular weight, critical properties, and, in the context of this project, their PC-SAFT parameters and mole fractions—so that the behavior of the overall fluid can be accurately modeled. This project focuses on using a fixed number of pseudo-components (e.g., five) to represent the fluid.

### PC-SAFT Equation of State

The **Perturbed-Chain Statistical Associating Fluid Theory (PC-SAFT)** is an advanced equation of state (EoS) used to calculate the thermodynamic properties of pure fluids and mixtures. It is particularly well-suited for complex fluids, including polymers and, relevant to this project, petroleum fluids.

PC-SAFT models molecules as chains of spherical segments. The model accounts for:
*   **Repulsive forces** between segments (hard-chain reference term, `Z_hc`).
*   **Attractive forces** (dispersion forces) between segments (dispersion term, `Z_disp`).
*   **Association effects** (e.g., hydrogen bonding) if present (association term, `Z_assoc`), though this term is often less critical for non-associating hydrocarbon systems.

For each pure component (or pseudo-component), PC-SAFT typically requires three main parameters:
*   `m`: The number of spherical segments per chain molecule (related to molecular size).
*   `sigma` (σ): The diameter of each segment (Angstroms).
*   `epsilon/k` (ε/k): The energy parameter, representing the depth of the potential well between non-bonded segments (Kelvin).

The compressibility factor `Z` (which relates pressure, volume, and temperature: `Z = PV/nRT`) is generally expressed as a sum of contributions:
`Z = 1 + Z_hc + Z_disp (+ Z_assoc for associating fluids)`

By calculating `Z` and its derivatives, various thermodynamic properties such as density, enthalpy, entropy, phase equilibria (vapor-liquid, liquid-liquid), and critical points can be determined.

## Machine Learning for Enhanced Characterization

The accuracy of PC-SAFT (and any EoS) in predicting fluid properties heavily relies on the quality of the input parameters for each component, especially for pseudo-components in a mixture. Determining these parameters (`m`, `sigma`, `epsilon_k`) for pseudo-components that best represent a complex petroleum fluid is a significant challenge. Traditional methods often rely on empirical correlations or extensive experimental data fitting.

This project proposes to leverage Machine Learning (ML) to improve and streamline the estimation of these PC-SAFT parameters for the pseudo-components.

### Proposed ML Workflow

The envisioned workflow for ML integration is as follows:

1.  **Inputs to the ML Model**:
    The ML model is designed to take readily available, measurable bulk petroleum properties as input. Examples include:
    *   API gravity
    *   Overall fluid viscosity (at specific conditions)
    *   Distillation curve data (e.g., T10, T50, T90 boiling points)
    *   Gas-Oil Ratio (GOR)
    *   Overall molecular weight of the fluid

2.  **ML Model Type**:
    A supervised learning approach, specifically a regression model, is envisioned. Potential candidates could include:
    *   Gradient Boosting Machines (e.g., XGBoost, LightGBM)
    *   Random Forests
    *   Neural Networks
    The current implementation in `src/ml_model.py` (`ParameterAdjustmentModel`) is a **placeholder**. It does not contain a trained model or the logic for training one. It simply returns dummy parameters to illustrate the workflow.

3.  **Outputs from the ML Model**:
    The ML model's primary output is a set of optimized or adjusted PC-SAFT parameters for each of the five pseudo-components used to represent the fluid. For each pseudo-component, these parameters are:
    *   `m` (number of segments)
    *   `sigma` (segment diameter)
    *   `epsilon_k` (energy parameter)

### Benefit of ML Integration

By training an ML model on a dataset of known petroleum fluids (where bulk properties are linked to "optimal" PC-SAFT parameters that accurately reproduce experimental data), the model can learn complex relationships. The goal is that for a new fluid, the ML model can predict a set of pseudo-component PC-SAFT parameters that are more accurate and physically consistent than those obtained from traditional, often generalized, correlations. This, in turn, should lead to more reliable fluid property predictions from the PC-SAFT EoS.

### Conceptual Flow Diagram

The overall process can be visualized as:

```
Input Bulk Fluid Properties (e.g., API, MW, T50)
           │
           ▼
[Machine Learning Model (src/ml_model.py - Placeholder)]
  (Predicts/adjusts parameters for 5 pseudo-components)
           │
           ▼
Adjusted PC-SAFT Parameters (m, sigma, epsilon_k for each of 5 pseudo-components)
           │
           ▼
[PC-SAFT Equation of State (src/pcsaft_wrapper.py - Placeholder)]
  (Calculates properties using adjusted parameters and mole fractions)
           │
           ▼
Calculated Fluid Properties (e.g., Density, Viscosity, Phase Behavior)
```

## Current Project Stage

The project, in its current form, provides the **foundational software framework and workflow orchestration** for the described petroleum characterization method. It establishes the conceptual structure and demonstrates the intended flow of data and calculations, but does not yet include fully implemented scientific computations.

This framework includes:
*   A **well-defined directory structure** for organizing code, data, examples, and tests.
*   **Placeholder modules** for key scientific components:
    *   PC-SAFT calculations (`src/pcsaft_wrapper.py`): Contains dummy functions that simulate PC-SAFT outputs without performing actual thermodynamic calculations.
    *   Machine Learning model (`src/ml_model.py`): Defines a `ParameterAdjustmentModel` class that returns placeholder PC-SAFT parameters instead of using a trained ML model.
*   The **core characterization logic** (`src/characterization.py`): Implements the `PetroleumCharacterization` class that orchestrates the workflow. It demonstrates how bulk properties would feed into the (placeholder) ML model, and how the resulting (placeholder) PC-SAFT parameters would then be used by the (placeholder) PC-SAFT wrapper.
*   **Example data structures**:
    *   Initial PC-SAFT parameters for pseudo-components (`data/pseudo_components_initial.json`).
    *   A conceptual layout for ML training data (`data/training_data_placeholder.csv`).
*   An **example script** (`examples/run_characterization_example.py`) that allows users to run the placeholder workflow and see the conceptual data flow and outputs.
*   **Unit tests** (`tests/test_characterization.py`) that verify the basic functionality and output structure of the existing placeholder logic and workflow orchestration.

**Emphasis on Future Work**: It is important to note that the detailed implementation of the PC-SAFT equations within the wrapper and the development, training, and validation of the specific machine learning model are significant **areas for future development**. The current project sets the stage for these implementations.

## Project Structure

The project is organized as follows:

```
petro_char_pcsaft_ml/
├── .gitignore                        # Files and directories to be ignored by Git
├── README.md                         # This file
├── data/                             # Datasets, initial parameters, and example training data
│   ├── pseudo_components_initial.json  # Initial PC-SAFT parameters for pseudo-components
│   └── training_data_placeholder.csv # Placeholder CSV for ML model training data format
├── docs/                             # Project documentation (currently a placeholder)
│   └── .gitkeep
├── examples/                         # Example scripts demonstrating usage
│   └── run_characterization_example.py
├── requirements.txt                  # Python dependencies
├── src/                              # Main Python source code
│   ├── __init__.py                   # Makes 'src' a Python package
│   ├── characterization.py           # Core workflow for fluid characterization
│   ├── ml_model.py                   # Placeholder for the ML model for parameter adjustment
│   └── pcsaft_wrapper.py             # Placeholder for direct PC-SAFT calculations/interactions
└── tests/                            # Unit and integration tests
    ├── __init__.py                   # Makes 'tests' a Python package
    ├── test_characterization.py      # Tests for the characterization workflow and ML model
    └── test_data/                    # Test-specific data files
        ├── __init__.py               # Makes 'test_data' a Python package
        └── dummy_params.json         # Dummy parameters for testing
```

## Setup Instructions

To set up the project locally, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd petro_char_pcsaft_ml
    ```
    (Replace `<repository_url>` with the actual URL of the repository.)

2.  **Create and activate a virtual environment** (recommended):
    It's good practice to use a virtual environment to manage project dependencies. Python 3.8+ is recommended.
    ```bash
    python -m venv venv
    ```
    Activate the environment:
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install dependencies**:
    Install the required Python packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The primary way to see the (current placeholder) workflow in action is by running the example script.

1.  **Run the example script**:
    Ensure you are in the project root directory (`petro_char_pcsaft_ml/`) and your virtual environment is activated.
    ```bash
    python examples/run_characterization_example.py
    ```

2.  **What the example does**:
    The `run_characterization_example.py` script demonstrates the intended workflow:
    *   It initializes the `PetroleumCharacterization` tool from `src.characterization`.
    *   It uses sample bulk fluid properties (like API gravity, molecular weight).
    *   It calls the characterization process, which internally uses the placeholder `ParameterAdjustmentModel` from `src.ml_model` to get "adjusted" PC-SAFT parameters for pseudo-components.
    *   It prints the initial inputs, the (currently dummy) adjusted parameters, and placeholder messages for where actual PC-SAFT calculations would occur.

## Running Tests

Unit tests are provided to verify the functionality of individual components.

1.  **Discover and run all tests**:
    From the project root directory (`petro_char_pcsaft_ml/`):
    ```bash
    python -m unittest discover -s tests
    ```

2.  **Run a specific test file**:
    ```bash
    python -m unittest tests.test_characterization
    ```

The tests will check the basic functionality of the `ParameterAdjustmentModel` and `PetroleumCharacterization` classes, including parameter loading and output structures.

## Key Components

*   `src/characterization.py`: Contains the `PetroleumCharacterization` class, which orchestrates the overall characterization workflow. It integrates the ML model and (conceptually) the PC-SAFT calculations.
*   `src/ml_model.py`: Defines the `ParameterAdjustmentModel` class. Currently, this is a **placeholder** that returns fixed dummy PC-SAFT parameters without any actual ML prediction.
*   `src/pcsaft_wrapper.py`: Intended to be a wrapper for a PC-SAFT calculation engine (e.g., `sgtpy` or another library). This is currently a **placeholder** with dummy functions that return fixed values.
*   `data/pseudo_components_initial.json`: A JSON file storing the initial (base) PC-SAFT parameters (`m`, `sigma`, `epsilon_k`) for a set of predefined pseudo-components.
*   `data/training_data_placeholder.csv`: A CSV file showing the expected format for data that could be used to train the `ParameterAdjustmentModel`. It includes columns for input fluid properties and target PC-SAFT parameters for multiple pseudo-components.
*   `examples/run_characterization_example.py`: A script that demonstrates how to use the `PetroleumCharacterization` tool with sample inputs.

## Future Work / Placeholders

This project is currently in an initial scaffolding phase. Several key areas are implemented as placeholders and require significant further development:

*   **Machine Learning Model (`src/ml_model.py`)**:
    *   The `ParameterAdjustmentModel` needs to be replaced with an actual ML model (e.g., using scikit-learn, TensorFlow, PyTorch).
    *   This model needs to be trained on relevant data (linking bulk properties to optimal PC-SAFT parameters for pseudo-components). The `training_data_placeholder.csv` provides a conceptual data structure.
*   **PC-SAFT Integration (`src/pcsaft_wrapper.py` and `src/characterization.py`)**:
    *   Actual PC-SAFT calculations need to be implemented. This involves choosing a PC-SAFT library/engine (like `sgtpy`, or implementing the equations directly).
    *   The `characterization.py` workflow must be updated to call this PC-SAFT engine with the ML-adjusted parameters to compute fluid properties (density, viscosity, phase behavior, etc.).
*   **Parameter Optimization**: The framework could be extended to include an optimization loop where the ML-predicted parameters are further refined by matching calculated PC-SAFT properties against experimental data.
*   **Data Expansion**: More comprehensive datasets for training and testing will be required.

## Contributing

Currently, this project is a conceptual framework. Future contributions could focus on implementing the "Future Work" items. (Further contribution guidelines to be defined).

## License

The license for this project is yet to be determined. (e.g., MIT, Apache 2.0).
