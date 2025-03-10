from dataclasses import dataclass


@dataclass
class ModelEvaluatorArtifact:
    trained_model_file_path : str
    new_model_is_better     : bool
    score_improves_by        : float
