from scripts.benchmark_dashboard import collect_benchmark_report, generate_demo_layer_metrics, main


def test_generate_demo_layer_metrics_has_expected_shape():
    layers = generate_demo_layer_metrics()

    assert len(layers) == 5
    assert layers[0]["layer"].startswith("Layer 1")
    assert layers[0]["roc_auc"] > 0.90
    assert layers[0]["f1_score"] > 0.80
    assert layers[0]["latency_ms"] > 0


def test_collect_benchmark_report_builds_summary():
    report = collect_benchmark_report(threshold=0.66)

    assert report["threshold"] == 0.66
    assert report["summary"]["best_layer"]
    assert len(report["layers"]) == 5
    assert report["summary"]["avg_roc_auc"] > 0.90
    assert report["summary"]["max_latency_ms"] > 100


def test_main_headless_mode_prints_json(capsys):
    exit_code = main(["--headless", "--threshold", "0.75"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert '"threshold": 0.75' in output
    assert '"avg_roc_auc"' in output
    assert '"layers"' in output
