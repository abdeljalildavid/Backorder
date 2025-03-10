from collections import namedtuple

ModelEvaluatorConfiguration = namedtuple("modelEvaluator",
                                      [
                                          "model_evaluator_dir_path",
                                          "model_report_file_path",
                                          "threshold", 
                                      ]
                                      )