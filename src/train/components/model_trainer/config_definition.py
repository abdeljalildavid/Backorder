from collections import namedtuple


ModelTrainerConfiguration = namedtuple("modelTrainer",
                                      [
                                          "model_trainer_dir_path",
                                          "model_object_file_path",
                                          "score",
                                          "cross_validation_value"

                                      ]
                                      )