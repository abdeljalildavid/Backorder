from dataclasses import dataclass


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path : str
    score_metric            : str
    train_score             :float
    test_score              :float