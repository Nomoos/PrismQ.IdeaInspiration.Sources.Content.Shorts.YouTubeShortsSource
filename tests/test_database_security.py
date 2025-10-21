"""Test database security and input validation."""

import pytest
from mod.database import Database


def test_order_by_validation():
    """Test that order_by parameter is properly validated."""
    db = Database(":memory:", interactive=False)
    
    # Insert test data
    db.insert_idea(
        source="test",
        source_id="1",
        title="Test Idea",
        score=10.0
    )
    
    # Valid order_by values should work
    valid_values = [
        "score DESC",
        "score ASC",
        "title",
        "created_at DESC",
        "id ASC"
    ]
    
    for order_val in valid_values:
        ideas = db.get_all_ideas(order_by=order_val)
        assert len(ideas) == 1, f"order_by='{order_val}' should work"
    
    # Invalid column names should raise ValueError
    with pytest.raises(ValueError):
        db.get_all_ideas(order_by="invalid_column DESC")
    
    # Invalid direction should raise ValueError
    with pytest.raises(ValueError):
        db.get_all_ideas(order_by="score INVALID")


def test_sql_injection_prevention():
    """Test that SQL injection is prevented in order_by parameter."""
    db = Database(":memory:", interactive=False)
    
    db.insert_idea(
        source="test",
        source_id="1",
        title="Test Idea",
        score=10.0
    )
    
    # These should either raise ValueError or default to safe order
    malicious_inputs = [
        "score; DROP TABLE ideas; --",
        "score DESC; DELETE FROM ideas; --",
        "1=1 OR 1=1",
    ]
    
    for malicious_input in malicious_inputs:
        # Should either raise ValueError or safely ignore the malicious part
        try:
            ideas = db.get_all_ideas(order_by=malicious_input)
            # If it doesn't raise an error, it should use the default
            # and the table should still exist
            assert len(ideas) == 1, "Table should still have data"
        except ValueError:
            # This is also acceptable - rejecting invalid input
            pass


def test_limit_validation():
    """Test that limit parameter is properly validated."""
    db = Database(":memory:", interactive=False)
    
    db.insert_idea(
        source="test",
        source_id="1",
        title="Test Idea",
        score=10.0
    )
    
    # Valid limits should work
    ideas = db.get_all_ideas(limit=1)
    assert len(ideas) == 1
    
    ideas = db.get_all_ideas(limit=10)
    assert len(ideas) == 1
    
    # Invalid limits should raise ValueError
    with pytest.raises(ValueError):
        db.get_all_ideas(limit=-1)
    
    with pytest.raises(ValueError):
        db.get_all_ideas(limit="invalid")


def test_order_by_edge_cases():
    """Test edge cases in order_by parameter."""
    db = Database(":memory:", interactive=False)
    
    # Insert test data
    for i in range(3):
        db.insert_idea(
            source="test",
            source_id=str(i),
            title=f"Test Idea {i}",
            score=float(i)
        )
    
    # Empty string should use default
    ideas = db.get_all_ideas(order_by="")
    assert len(ideas) == 3
    
    # Whitespace should be handled
    ideas = db.get_all_ideas(order_by="  score  DESC  ")
    assert len(ideas) == 3
    assert ideas[0]['score'] == 2.0  # Highest score first
    
    # Single column without direction should add DESC
    ideas = db.get_all_ideas(order_by="score")
    assert len(ideas) == 3
    assert ideas[0]['score'] == 2.0  # Should default to DESC
