"""Tests for Pipeline."""

import pytest

from sotai import FeatureType, Metric, Pipeline, TargetType

from .fixtures import (  # pylint: disable=unused-import
    fixture_test_categories,
    fixture_test_data,
    fixture_test_feature_configs,
    fixture_test_feature_names,
    fixture_test_target,
)


@pytest.mark.parametrize(
    "target_type,expected_primary_metric",
    [(TargetType.CLASSIFICATION, Metric.AUC), (TargetType.REGRESSION, Metric.MSE)],
)
def test_init(
    test_feature_names: fixture_test_feature_names,
    test_target: fixture_test_target,
    target_type,
    expected_primary_metric,
):
    """Tests pipeline initialization for a classification target."""
    pipeline = Pipeline(test_feature_names, test_target, target_type)
    assert pipeline.name == f"{test_target}_{target_type}"
    assert pipeline.target == test_target
    assert pipeline.target_type == target_type
    assert pipeline.primary_metric == expected_primary_metric
    assert len(pipeline.feature_configs) == 2
    numerical_config = pipeline.feature_configs["numerical"]
    assert numerical_config.name == "numerical"
    assert numerical_config.type == FeatureType.NUMERICAL
    categorical_config = pipeline.feature_configs["categorical"]
    assert categorical_config.name == "categorical"
    # Note: we expect the default config to be numerical if not specified.
    assert categorical_config.type == FeatureType.NUMERICAL


def test_init_with_categories(
    test_feature_names: fixture_test_feature_names,
    test_target: fixture_test_target,
    test_categories: fixture_test_categories,
):
    """Tests pipeline initialization with specified categories."""
    pipeline = Pipeline(
        test_feature_names,
        test_target,
        TargetType.CLASSIFICATION,
        categories={"categorical": test_categories},
    )
    categorical_config = pipeline.feature_configs["categorical"]
    assert categorical_config.name == "categorical"
    assert categorical_config.type == FeatureType.CATEGORICAL
    assert categorical_config.categories == test_categories


def test_prepare(
    test_data: fixture_test_data,
    test_feature_names: fixture_test_feature_names,
    test_target: fixture_test_target,
    test_categories: fixture_test_target,
):
    """Tests the pipeline prepare function."""
    pipeline = Pipeline(
        test_feature_names, test_target, target_type=TargetType.CLASSIFICATION
    )
    # We set shuffle to false to ensure the data is split in the same way.
    pipeline.shuffle_data = False
    pipeline.dataset_split.train = 80
    pipeline.dataset_split.val = 10
    pipeline.dataset_split.test = 10
    dataset, pipeline_config = pipeline.prepare(test_data)
    assert pipeline_config.id == 0
    categorical_config = pipeline_config.feature_configs["categorical"]
    assert categorical_config.name == "categorical"
    assert categorical_config.type == FeatureType.CATEGORICAL
    assert categorical_config.categories == test_categories
    assert dataset.id == 0
    assert dataset.pipeline_config_id == pipeline_config.id
    num_examples = len(test_data)
    num_training_examples = int(num_examples * pipeline.dataset_split.train / 100)
    num_val_examples = int(num_examples * pipeline.dataset_split.val / 100)
    assert dataset.prepared_data.train.equals(test_data.iloc[:num_training_examples])
    assert dataset.prepared_data.val.equals(
        test_data.iloc[num_training_examples : num_training_examples + num_val_examples]
    )
    assert dataset.prepared_data.test.equals(
        test_data.iloc[num_training_examples + num_val_examples :]
    )


@pytest.mark.parametrize(
    "target_type",
    [
        (TargetType.CLASSIFICATION),
        (TargetType.REGRESSION),
    ],
)
def test_train_calibrated_linear_model(
    test_data,
    test_feature_names: fixture_test_feature_names,
    test_target: fixture_test_target,
    target_type,
):
    """Tests pipeline training for calibrated linear regression model."""
    pipeline = Pipeline(test_feature_names, test_target, target_type)
    pipeline.shuffle_data = False
    pipeline.dataset_split.train = 60
    pipeline.dataset_split.val = 20
    pipeline.dataset_split.test = 20
    trained_model = pipeline.train(test_data)
    assert len(pipeline.configs) == 1
    assert len(pipeline.datasets) == 1
    assert trained_model
    assert trained_model.dataset_id == 0
    assert pipeline.datasets[trained_model.dataset_id]
    assert trained_model.pipeline_config.id == 0
    assert pipeline.configs[trained_model.pipeline_config.id]


def test_pipeline_save_load(
    test_data: fixture_test_data,
    test_feature_names: fixture_test_feature_names,
    test_target: fixture_test_target,
    tmp_path,
):
    """Tests that an instance of `Pipeline` can be successfully saved and loaded."""
    pipeline = Pipeline(test_feature_names, test_target, TargetType.CLASSIFICATION)
    _ = pipeline.train(test_data)
    pipeline.save(tmp_path)
    loaded_pipeline = Pipeline.load(tmp_path)
    assert isinstance(loaded_pipeline, Pipeline)
    assert loaded_pipeline.name == pipeline.name
    assert loaded_pipeline.target == pipeline.target
    assert loaded_pipeline.target_type == pipeline.target_type
    assert loaded_pipeline.primary_metric == pipeline.primary_metric
    assert loaded_pipeline.feature_configs == pipeline.feature_configs
    assert loaded_pipeline.configs == pipeline.configs
    for dataset_id, loaded_dataset in loaded_pipeline.datasets.items():
        dataset = pipeline.datasets[dataset_id]
        assert loaded_dataset.id == dataset.id
        assert loaded_dataset.pipeline_config_id == dataset.pipeline_config_id
        assert loaded_dataset.prepared_data.train.equals(dataset.prepared_data.train)
        assert loaded_dataset.prepared_data.val.equals(dataset.prepared_data.val)
        assert loaded_dataset.prepared_data.test.equals(dataset.prepared_data.test)
