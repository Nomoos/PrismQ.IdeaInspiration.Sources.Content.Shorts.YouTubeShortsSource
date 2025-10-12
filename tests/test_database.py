"""Tests for database module."""

import pytest
import tempfile
import os
from src.database import Database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as f:
        db_path = f.name
    
    db = Database(db_path)
    yield db
    
    db.close()
    if os.path.exists(db_path):
        os.unlink(db_path)


def test_database_initialization(temp_db):
    """Test database initialization creates tables."""
    cursor = temp_db.connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ideas'")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == 'ideas'


def test_insert_idea(temp_db):
    """Test inserting an idea."""
    success = temp_db.insert_idea(
        source='test',
        source_id='123',
        title='Test Idea',
        description='Test description',
        tags='tag1,tag2',
        score=85.5,
        score_dictionary={'test': 1.0}
    )
    assert success is True


def test_insert_duplicate_idea(temp_db):
    """Test that duplicate ideas are updated, not inserted twice."""
    # Insert first idea
    temp_db.insert_idea(
        source='test',
        source_id='123',
        title='Original Title',
        description='Original description',
        score=50.0
    )
    
    # Insert duplicate with updated info
    temp_db.insert_idea(
        source='test',
        source_id='123',
        title='Updated Title',
        description='Updated description',
        score=75.0
    )
    
    # Verify only one entry exists
    ideas = temp_db.get_all_ideas()
    assert len(ideas) == 1
    assert ideas[0]['title'] == 'Updated Title'
    assert ideas[0]['score'] == 75.0


def test_get_idea(temp_db):
    """Test retrieving a specific idea."""
    temp_db.insert_idea(
        source='test',
        source_id='456',
        title='Test Idea',
        description='Test description'
    )
    
    idea = temp_db.get_idea('test', '456')
    assert idea is not None
    assert idea['title'] == 'Test Idea'
    assert idea['source'] == 'test'
    assert idea['source_id'] == '456'


def test_get_nonexistent_idea(temp_db):
    """Test retrieving a non-existent idea returns None."""
    idea = temp_db.get_idea('test', 'nonexistent')
    assert idea is None


def test_get_all_ideas(temp_db):
    """Test retrieving all ideas."""
    # Insert multiple ideas
    temp_db.insert_idea(source='test1', source_id='1', title='Idea 1', score=90.0)
    temp_db.insert_idea(source='test1', source_id='2', title='Idea 2', score=70.0)
    temp_db.insert_idea(source='test2', source_id='3', title='Idea 3', score=80.0)
    
    ideas = temp_db.get_all_ideas()
    assert len(ideas) == 3


def test_get_all_ideas_with_limit(temp_db):
    """Test retrieving ideas with limit."""
    # Insert multiple ideas
    for i in range(10):
        temp_db.insert_idea(source='test', source_id=str(i), title=f'Idea {i}', score=float(i))
    
    ideas = temp_db.get_all_ideas(limit=5)
    assert len(ideas) == 5


def test_context_manager(temp_db):
    """Test database context manager."""
    db_path = temp_db.db_path
    temp_db.close()
    
    with Database(db_path) as db:
        success = db.insert_idea(
            source='test',
            source_id='context',
            title='Context Test'
        )
        assert success is True
    
    # Verify connection is closed
    # Note: We can't directly test if connection is closed in SQLite
    # but we can verify data was saved
    db2 = Database(db_path)
    idea = db2.get_idea('test', 'context')
    assert idea is not None
    db2.close()
