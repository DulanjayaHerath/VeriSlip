"""Configuration contract tests for the staging deployment pipeline."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_render_blueprint_is_health_checked_and_secret_safe():
    blueprint = (ROOT / "render.yaml").read_text(encoding="utf-8")
    assert "name: verislip-staging" in blueprint
    assert "runtime: docker" in blueprint
    assert "healthCheckPath: /health" in blueprint
    assert "autoDeploy: false" in blueprint
    assert "key: VERISLIP_API_KEY_HASHES\n        sync: false" in blueprint
    assert "VERISLIP_SYNTHETIC_GENERATOR_ENABLED" in blueprint
    assert "value: \"0\"" in blueprint
    assert "verislip-dev-key" not in blueprint
    assert "password" not in blueprint.lower()


def test_deploy_runs_only_after_ci_and_uses_bounded_health_checks():
    workflow = (ROOT / ".github" / "workflows" / "deploy-staging.yml").read_text(
        encoding="utf-8"
    )
    assert "workflows: [VeriSlip CI]" in workflow
    assert "github.event.workflow_run.conclusion == 'success'" in workflow
    assert "secrets.RENDER_STAGING_DEPLOY_HOOK_URL" in workflow
    assert "vars.VERISLIP_STAGING_URL" in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "--max-time 30" in workflow
    assert "Waiting for staging deployment" in workflow
    assert "echo \"$DEPLOY_HOOK\"" not in workflow


def test_runbook_documents_setup_verification_and_rollback():
    runbook = (ROOT / "docs" / "DEPLOYMENT_STAGING.md").read_text(encoding="utf-8")
    for required in (
        "One-time setup",
        "Deployment and verification",
        "Rollback and troubleshooting",
        "VERISLIP_API_KEY_HASHES",
        "RENDER_STAGING_DEPLOY_HOOK_URL",
    ):
        assert required in runbook
