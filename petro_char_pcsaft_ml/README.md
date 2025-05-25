# PetroChar PCSAFT ML

## Purpose

This project aims to develop a tool for petroleum fluid characterization using a combination of Machine Learning (ML) techniques and the Perturbed-Chain Statistical Associating Fluid Theory (PC-SAFT) equation of state.

The core idea is to:
1.  Use ML models to predict/adjust key parameters of pseudo-components based on readily available experimental data (e.g., API gravity, molecular weight, boiling points).
2.  Employ these ML-derived parameters within a PC-SAFT framework to model thermodynamic and transport properties of petroleum fluids.
3.  (Future) Optimize the pseudo-component parameters by fitting them to experimental fluid property data.

This approach seeks to provide a more accurate and efficient characterization workflow compared to traditional methods.

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
*   `src/ml_model.py`: Defines the `ParameterAdjustmentModel` class. Currently, this is a **placeholder** that returns dummy adjusted PC-SAFT parameters without any actual ML prediction.
*   `src/pcsaft_wrapper.py`: Intended to be a wrapper for a PC-SAFT calculation engine (e.g., `sgtpy` or another library). This is currently a **placeholder** with dummy functions.
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
