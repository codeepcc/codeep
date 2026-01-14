import pytest
from codeep_upgrade import upgrade_optimizer

def test_optimize_basic():
    """Test basic optimization functionality."""
    result = upgrade_optimizer.optimize("v2.1.0")
    
    assert isinstance(result, dict)
    assert result["target_version"] == "v2.1.0"
    assert "recommended_steps" in result
    assert "risks" in result
    assert "recommendations" in result
    assert isinstance(result["recommended_steps"], list)
    assert len(result["recommended_steps"]) > 0

def test_optimize_empty_version():
    """Test optimization with empty version string."""
    result = upgrade_optimizer.optimize("")
    
    assert isinstance(result, dict)
    assert result["target_version"] == ""

def test_add_dependency():
    """Test adding dependencies."""
    upgrade_optimizer.add_dependency("numpy", "1.24.0")
    assert "numpy" in upgrade_optimizer.dependencies
    assert upgrade_optimizer.dependencies["numpy"] == "1.24.0"

def test_compatibility_report():
    """Test compatibility report generation."""
    upgrade_optimizer.add_dependency("requests", "2.31.0")
    report = upgrade_optimizer.get_compatibility_report("v2.1.0")
    
    assert report["target_version"] == "v2.1.0"
    assert "requests" in report["compatible_dependencies"]
    assert len(report["incompatible_dependencies"]) == 0