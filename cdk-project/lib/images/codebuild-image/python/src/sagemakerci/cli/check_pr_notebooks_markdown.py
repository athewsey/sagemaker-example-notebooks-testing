#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys

import language_tool_python

from sagemakerci.cli.run_pr_notebooks import notebook_filenames


allow_list = {
    "Alexa",
    "Amazon",
    "AWS",
    "aws",
    "Amplify",
    "API",
    "Gateway",
    "App" "AppFlow",
    "AppStream",
    "AppSync",
    "ARN",
    "arn",
    "Athena",
    "A2I",
    "Aurora",
    "Backint",
    "Blockchain",
    "Blox",
    "BYOC",
    "ACM",
    "Chatbot",
    "VPN",
    "CDK",
    "Cloud9",
    "CloudFormation",
    "CloudFront",
    "CloudHSM",
    "CloudSearch",
    "CloudShell",
    "CloudTrail",
    "CloudWatch",
    "CodeArtifact",
    "CodeBuild",
    "CodeCommit",
    "CodeDeploy",
    "CodeGuru",
    "CodePipeline",
    "CodeStar",
    "Cognito",
    "CLI",
    "Comprehend",
    "Config",
    "Corretto",
    "DataSync",
    "DLAMI",
    "DLAMIs",
    "DLC",
    "DLCs",
    "DeepComposer",
    "DeepLens",
    "DeepRacer",
    "DevPay",
    "DMS",
    "DocumentDB",
    "DynamoDB",
    "EC2",
    "EBS",
    "ECR",
    "ECS",
    "Kubernetes",
    "EKS",
    "EFS",
    "Transcoder",
    "Elasticache",
    "ES",
    "EMR",
    "EventBridge",
    "Fargate",
    "FreeRTOS",
    "FSx",
    "Lustre",
    "GameLift",
    "Grafana",
    "Greengrass",
    "GovCloud",
    "GuardDuty",
    "HealthLake",
    "Honeycode",
    "IAM",
    "Import/Export",
    "IoT",
    "LoRaWAN",
    "SiteWise",
    "1-Click",
    "IVS",
    "Kendra",
    "KMS",
    "Keyspaces",
    "Kinesis",
    "Lambda",
    "Lex",
    "Lightsail",
    "Lookout",
    "Lumberyard",
    "Macie",
    "Apache",
    "Kafka",
    "MSK",
    "Airflow",
    "vCenter",
    "MTurk",
    "MediaConnect",
    "MediaConvert",
    "MediaLive",
    "MediaPackage",
    "MediaStore",
    "MediaTailor",
    "Monitron",
    "MQ",
    "OpsWorks",
    "ParallelCluster",
    "Polly",
    "PCA",
    "AMP",
    "QLDB",
    "QuickSight",
    "Redshift",
    "Rekognition",
    "RDS",
    "RAM",
    "RoboMaker",
    "SageMaker",
    "JumpStart",
    "Serverless",
    "SAM",
    "SES",
    "SNS",
    "SQS",
    "S3",
    "SWF",
    "SimpleDB",
    "SSO",
    "Sumerian",
    "Android",
    "C++",
    "iOS",
    "JavaScript",
    ".NET",
    "Boto3",
    "boto3",
    "Python",
    "Textract",
    "Timestream",
    "PowerShell",
    "VPC",
    "WAF",
    "Well-Architected",
    "WorkDocs",
    "WorkLink",
    "WorkMail",
    "WorkSpaces",
    "WAM",
    "X-Ray",
    "Roboschool",
    "utils",
    "Horovod",
    "Keras",
    "Gluon",
    "ONNX",
    "RNN",
    "CNN",
    "LSTM",
    "NumPy",
    "SciPy",
    "hyperparameter",
    "hyperparameters",
    "Hyperparameter",
    "Hyperparameters",
    "csv",
    "CSV",
    "uri",
    "URI",
    "jsonl",
    "json",
    "JSON",
    "ContentType",
    "serializers",
    "deserializers",
    "baselining",
    "Baselining",
    "smdebug",
    "sagemaker",
    "FeatureGroup",
    "AthenaQuery",
    "IngestionManagerPandas",
    "FeatureDefinition",
    "FractionalFeatureDefinition",
    "IntegralFeatureDefinition",
    "StringFeatureDefinition",
    "FeatureTypeEnum",
    "Config",
    "config",
    "configs",
    "DataCatalogConfig",
    "OfflineStoreConfig",
    "OnlineStoreConfig",
    "OnlineStoreSecurityConfig",
    "S3StorageConfig",
    "FeatureValue",
    "AnalyticsMetricsBase",
    "HyperparameterTuningJobAnalytics",
    "TrainingJobAnalytics",
    "ExperimentAnalytics",
    "AutoML",
    "AutoMLInput",
    "AutoMLJob",
    "CandidateEstimator",
    "CandidateStep",
    "RuleBase",
    "ProfilerRule",
    "CollectionConfig",
    "DebuggerHookConfig",
    "TensorBoardOutputConfig",
    "ProfilerConfig",
    "FrameworkProfile",
    "DetailedProfilingConfig",
    "DataloaderProfilingConfig",
    "PythonProfilingConfig",
    "PythonProfiler",
    "cProfileTimer",
    "StepRange",
    "TimeRange",
    "EstimatorBase",
    "Estimator",
    "Framework",
    "AlgorithmEstimator",
    "HyperparameterTuner",
    "ContinuousParameter",
    "IntegerParameter",
    "CategoricalParameter",
    "ParameterRange",
    "Processor",
    "ScriptProcessor",
    "ProcessingJob",
    "ProcessingInput",
    "ProcessingOutput",
    "RunArgs",
    "FeatureStoreOutput",
    "PySparkProcessor",
    "PySpark",
    "SparkJarProcessor",
    "FileType",
    "DataConfig",
    "BiasConfig",
    "ModelConfig",
    "ModelPredictedLabelConfig",
    "ExplainabilityConfig",
    "SHAPConfig",
    "SHAP",
    "SageMakerClarifyProcessor",
    "DistributedDataParallel",
    "DistributedModel",
    "StepOutput",
    "DistributedOptimizer",
    "BaseDeserializer",
    "SimpleBaseDeserializer",
    "StringDeserializer",
    "BytesDeserializer",
    "CSVDeserializer",
    "StreamDeserializer",
    "NumpyDeserializer",
    "JSONDeserializer",
    "PandasDeserializer",
    "JSONLinesDeserializer",
    "Model",
    "FrameworkModel",
    "ModelPackage",
    "ModelMonitor",
    "DefaultModelMonitor",
    "ModelQualityMonitor",
    "BaseliningJob",
    "MonitoringExecution",
    "EndpointInput",
    "MonitoringOutput",
    "ModelMonitoringFile",
    "Statistics",
    "Constraints",
    "ConstraintViolations",
    "DatasetFormat",
    "DataCaptureConfig",
    "CronExpressionGenerator",
    "MultiDataModel",
    "PipelineModel",
    "Predictor",
    "BaseSerializer",
    "SimpleBaseSerializer",
    "CSVSerializer",
    "NumpySerializer",
    "JSONSerializer",
    "IdentitySerializer",
    "JSONLinesSerializer",
    "SparseMatrixSerializer",
    "LibSVMSerializer",
    "LibSVM",
    "Transformer",
    "TrainingInput",
    "ShuffleConfig",
    "CreateModelInput",
    "TransformInput",
    "FileSystemInput",
    "NetworkConfig",
    "S3Uploader",
    "S3Downloader",
    "LogState",
    "Session",
    "MXNet",
    "MXNetModel",
    "MXNetPredictor",
    "HuggingFace",
    "PyTorch",
    "PyTorchModel",
    "PyTorchPredictor",
    "RLEstimator",
    "RLToolkit",
    "RLFramework",
    "SKLearn",
    "SKLearnModel",
    "SKLearnPredictor",
    "SKLearnProcessor",
    "SparkMLModel",
    "SparkMLPredictor",
    "TensorFlow",
    "TensorFlowModel",
    "TensorFlowPredictor",
    "XGBoost",
    "XGBoostModel",
    "XGBoostPredictor",
    "AmazonAlgorithmEstimatorBase",
    "FactorizationMachines",
    "FactorizationMachinesModel",
    "FactorizationMachinesPredictor",
    "IPInsights",
    "IPInsightsModel",
    "IPInsightsPredictor",
    "KMeans",
    "KMeansModel",
    "KMeansPredictor",
    "KNN",
    "KNNModel",
    "KNNPredictor",
    "LDA",
    "LDAModel",
    "LDAPredictor",
    "LinearLearner",
    "LinearLearnerModel",
    "LinearLearnerPredictor",
    "NTM",
    "NTMModel",
    "NTMPredictor",
    "Object2Vec",
    "Object2VecModel",
    "PCA",
    "PCAModel",
    "PCAPredictor",
    "RandomCutForest",
    "RandomCutForestModel",
    "RandomCutForestPredictor",
    "ConditionStep",
    "JsonGet",
    "ConditionTypeEnum",
    "Condition",
    "ConditionComparison",
    "ConditionEquals",
    "ConditionGreaterThan",
    "ConditionGreaterThanOrEqualTo",
    "ConditionLessThan",
    "ConditionLessThanOrEqualTo",
    "ConditionIn",
    "ConditionNot",
    "ConditionOr",
    "Entity",
    "DefaultEnumMeta",
    "Expression",
    "ExecutionVariable",
    "ExecutionVariables",
    "Join",
    "ParameterTypeEnum",
    "Parameter",
    "ParameterString",
    "ParameterInteger",
    "ParameterFloat",
    "Pipeline",
    "PropertiesMeta",
    "Properties",
    "PropertiesList",
    "PropertyFile",
    "StepCollection",
    "RegisterModel",
    "EstimatorTransformer",
    "StepTypeEnum",
    "Step",
    "TrainingStep",
    "CreateModelStep",
    "TransformStep",
    "ProcessingStep",
    "ProfilerReport",
    "BatchSize",
    "CPUBottleneck",
    "GPUMemoryIncrease",
    "IOBottleneck",
    "LoadBalancing",
    "LowGPUUtilization",
    "OverallSystemUsage",
    "MaxInitializationTime",
    "OverallFrameworkMetrics",
    "StepOutlier",
    "CreateXGBoostReport",
    "DeadRelu",
    "ExplodingTensor",
    "PoorWeightInitialization",
    "SaturatedActivation",
    "VanishingGradient",
    "WeightUpdateRatio",
    "AllZero",
    "ClassImbalance",
    "LossNotDecreasing",
    "Overfit",
    "Overtraining",
    "SimilarAcrossRuns",
    "StalledTrainingRule",
    "TensorVariance",
    "UnchangedTensor",
    "CheckInputImages",
    "NLPSequenceRatio",
    "Confusion",
    "FeatureImportanceOverweight",
    "TreeDepth",
    "stdin",
    "stdout",
    "BlazingText",
    "SparkML",
    "Jupyter",
    "JupyterLab",
    "ml",
    "ML",
    "xlarge",
    "GPU",
    "checkpoint",
    "checkpointed",
}

rules_to_ignore = {
    "PUNCTUATION_PARAGRAPH_END",
    "WORD_CONTAINS_UNDERSCORE",
    "DASH_RULE",
    "EN_QUOTES",
    "WRONG_APOSTROPHE",
}


def parse_args(args):
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.set_defaults(func=lambda x: parser.print_usage())
    parser.add_argument("--pr", help="Pull request number", type=int, required=True)

    parsed = parser.parse_args(args)
    if not parsed.pr:
        parser.error("--pr required")

    return parsed


def markdown_cells(notebook):
    with open(notebook) as notebook_file:
        cells = json.load(notebook_file)["cells"]
    md_cells = []
    for cell in cells:
        if cell["cell_type"] == "markdown":
            md_cells.append(cell["source"])
    return md_cells


def check_grammar(notebook):
    tool = language_tool_python.LanguageTool("en-US")

    report = []

    cells = markdown_cells(notebook)
    for cell in cells:
        code_block = False
        for line in cell:
            stripped_line = line.rstrip().strip(" #*")
            if stripped_line in ("```python", "```bash", "```"):
                code_block = not code_block
            if code_block:
                continue
            code_substituted_line = re.sub(
                "(`)\1{2,}[^`]*(`)\1{2,}|`[^`]*`", "[code]", stripped_line
            )
            matches = tool.check(code_substituted_line)
            report.extend(matches)

    is_correctly_spelled = lambda rule: rule.ruleIssueType == "misspelling" and (
        rule.matchedText in allow_list
        or "-" in rule.matchedText
        or "_" in rule.matchedText
        or "$" in rule.matchedText
    )
    report = [rule for rule in report if not is_correctly_spelled(rule)]

    is_ignored_rule = lambda rule: rule.ruleId in rules_to_ignore
    report = [rule for rule in report if not is_ignored_rule(rule)]

    return report


def main():
    args = parse_args(sys.argv[1:])

    failures = {}

    for notebook in notebook_filenames(args.pr):
        report = check_grammar(notebook)
        if report:
            failures[notebook] = report
            basename = os.path.basename(notebook)
            print("\n" * 2)
            print(f"* {basename} " + "*" * (97 - len(basename)))
            print()
            print("\n\n".join([str(match) for match in report]))

    print("\n" * 2)
    print("-" * 100)
    if len(failures) > 0:
        raise Exception(
            "One or more notebooks did not pass the spelling and grammar check. Please see above for error messages. "
            "To fix the text in your notebook, use language_tool_python.utils.correct: https://pypi.org/project/language-tool-python/"
        )


if __name__ == "__main__":
    main()
