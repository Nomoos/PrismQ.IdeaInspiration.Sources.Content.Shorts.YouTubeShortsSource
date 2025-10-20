"""Tests for the YouTubeShortsSource model and DBContext."""

import pytest
import tempfile
import os
import json
from datetime import datetime
from mod.Model import YouTubeShortsSource, DBContext


@pytest.fixture
def temp_db_context():
    """Create a temporary database context for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as f:
        db_path = f.name
    
    db_context = DBContext(db_path)
    yield db_context
    
    db_context.close()
    if os.path.exists(db_path):
        os.unlink(db_path)


class TestYouTubeShortsSourceModel:
    """Tests for the YouTubeShortsSource model."""
    
    def test_model_creation(self, temp_db_context):
        """Test creating a model instance."""
        record = temp_db_context.create(
            source='youtube',
            source_id='test123',
            title='Test Video',
            description='Test description',
            tags='tag1,tag2',
            score=85.5
        )
        
        assert record is not None
        assert record.source == 'youtube'
        assert record.source_id == 'test123'
        assert record.title == 'Test Video'
        assert record.description == 'Test description'
        assert record.tags == 'tag1,tag2'
        assert record.score == 85.5
    
    def test_model_with_score_dictionary(self, temp_db_context):
        """Test model with score dictionary."""
        score_dict = {
            'engagement_rate': 0.85,
            'views': 10000,
            'likes': 500
        }
        
        record = temp_db_context.create(
            source='youtube',
            source_id='test456',
            title='Test Video 2',
            score_dictionary=score_dict
        )
        
        assert record is not None
        retrieved_dict = record.get_score_dict()
        assert retrieved_dict == score_dict
    
    def test_model_to_dict(self, temp_db_context):
        """Test converting model to dictionary."""
        record = temp_db_context.create(
            source='youtube',
            source_id='test789',
            title='Test Video 3',
            score=75.0
        )
        
        record_dict = record.to_dict()
        assert record_dict['source'] == 'youtube'
        assert record_dict['source_id'] == 'test789'
        assert record_dict['title'] == 'Test Video 3'
        assert record_dict['score'] == 75.0
        assert 'created_at' in record_dict
        assert 'updated_at' in record_dict
    
    def test_model_repr(self, temp_db_context):
        """Test model string representation."""
        record = temp_db_context.create(
            source='youtube',
            source_id='test_repr',
            title='Test Video for Repr'
        )
        
        repr_str = repr(record)
        assert 'YouTubeShortsSource' in repr_str
        assert 'youtube' in repr_str
        assert 'test_repr' in repr_str


class TestDBContextCRUD:
    """Tests for DBContext CRUD operations."""
    
    def test_create(self, temp_db_context):
        """Test create operation."""
        record = temp_db_context.create(
            source='youtube',
            source_id='create_test',
            title='Create Test'
        )
        
        assert record is not None
        assert record.id is not None
        assert record.source == 'youtube'
        assert record.source_id == 'create_test'
    
    def test_create_duplicate(self, temp_db_context):
        """Test that creating duplicate records fails."""
        temp_db_context.create(
            source='youtube',
            source_id='duplicate',
            title='First Record'
        )
        
        # Try to create duplicate
        duplicate = temp_db_context.create(
            source='youtube',
            source_id='duplicate',
            title='Duplicate Record'
        )
        
        assert duplicate is None
    
    def test_read(self, temp_db_context):
        """Test read operation."""
        created = temp_db_context.create(
            source='youtube',
            source_id='read_test',
            title='Read Test'
        )
        
        retrieved = temp_db_context.read('youtube', 'read_test')
        
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == 'Read Test'
    
    def test_read_nonexistent(self, temp_db_context):
        """Test reading non-existent record."""
        record = temp_db_context.read('youtube', 'nonexistent')
        assert record is None
    
    def test_read_by_id(self, temp_db_context):
        """Test read by ID operation."""
        created = temp_db_context.create(
            source='youtube',
            source_id='id_test',
            title='ID Test'
        )
        
        retrieved = temp_db_context.read_by_id(created.id)
        
        assert retrieved is not None
        assert retrieved.source_id == 'id_test'
        assert retrieved.title == 'ID Test'
    
    def test_update(self, temp_db_context):
        """Test update operation."""
        temp_db_context.create(
            source='youtube',
            source_id='update_test',
            title='Original Title',
            score=50.0
        )
        
        updated = temp_db_context.update(
            source='youtube',
            source_id='update_test',
            title='Updated Title',
            score=75.0
        )
        
        assert updated is not None
        assert updated.title == 'Updated Title'
        assert updated.score == 75.0
    
    def test_update_nonexistent(self, temp_db_context):
        """Test updating non-existent record."""
        result = temp_db_context.update(
            source='youtube',
            source_id='nonexistent',
            title='Should Not Work'
        )
        
        assert result is None
    
    def test_upsert_create(self, temp_db_context):
        """Test upsert creating a new record."""
        record = temp_db_context.upsert(
            source='youtube',
            source_id='upsert_new',
            title='New Record'
        )
        
        assert record is not None
        assert record.title == 'New Record'
    
    def test_upsert_update(self, temp_db_context):
        """Test upsert updating an existing record."""
        temp_db_context.create(
            source='youtube',
            source_id='upsert_existing',
            title='Original',
            score=50.0
        )
        
        updated = temp_db_context.upsert(
            source='youtube',
            source_id='upsert_existing',
            title='Updated',
            score=75.0
        )
        
        assert updated is not None
        assert updated.title == 'Updated'
        assert updated.score == 75.0
        
        # Verify only one record exists
        count = temp_db_context.count()
        assert count == 1
    
    def test_delete(self, temp_db_context):
        """Test delete operation."""
        temp_db_context.create(
            source='youtube',
            source_id='delete_test',
            title='To Be Deleted'
        )
        
        result = temp_db_context.delete('youtube', 'delete_test')
        assert result is True
        
        # Verify deletion
        record = temp_db_context.read('youtube', 'delete_test')
        assert record is None
    
    def test_delete_nonexistent(self, temp_db_context):
        """Test deleting non-existent record."""
        result = temp_db_context.delete('youtube', 'nonexistent')
        assert result is False
    
    def test_list_all(self, temp_db_context):
        """Test listing all records."""
        temp_db_context.create(source='youtube', source_id='1', title='Video 1', score=90.0)
        temp_db_context.create(source='youtube', source_id='2', title='Video 2', score=70.0)
        temp_db_context.create(source='youtube', source_id='3', title='Video 3', score=80.0)
        
        records = temp_db_context.list_all()
        
        assert len(records) == 3
        # Should be ordered by score descending by default
        assert records[0].score == 90.0
        assert records[1].score == 80.0
        assert records[2].score == 70.0
    
    def test_list_all_with_limit(self, temp_db_context):
        """Test listing records with limit."""
        for i in range(10):
            temp_db_context.create(
                source='youtube',
                source_id=f'video_{i}',
                title=f'Video {i}',
                score=float(i)
            )
        
        records = temp_db_context.list_all(limit=5)
        assert len(records) == 5
    
    def test_list_all_ascending(self, temp_db_context):
        """Test listing records in ascending order."""
        temp_db_context.create(source='youtube', source_id='1', title='Video 1', score=90.0)
        temp_db_context.create(source='youtube', source_id='2', title='Video 2', score=70.0)
        temp_db_context.create(source='youtube', source_id='3', title='Video 3', score=80.0)
        
        records = temp_db_context.list_all(ascending=True)
        
        assert len(records) == 3
        assert records[0].score == 70.0
        assert records[1].score == 80.0
        assert records[2].score == 90.0
    
    def test_count(self, temp_db_context):
        """Test count operation."""
        assert temp_db_context.count() == 0
        
        temp_db_context.create(source='youtube', source_id='1', title='Video 1')
        temp_db_context.create(source='youtube', source_id='2', title='Video 2')
        
        assert temp_db_context.count() == 2
    
    def test_count_by_source(self, temp_db_context):
        """Test count by source operation."""
        temp_db_context.create(source='youtube', source_id='1', title='YouTube 1')
        temp_db_context.create(source='youtube', source_id='2', title='YouTube 2')
        temp_db_context.create(source='tiktok', source_id='3', title='TikTok 1')
        
        assert temp_db_context.count_by_source('youtube') == 2
        assert temp_db_context.count_by_source('tiktok') == 1
        assert temp_db_context.count_by_source('instagram') == 0
    
    def test_clear_all(self, temp_db_context):
        """Test clearing all records."""
        temp_db_context.create(source='youtube', source_id='1', title='Video 1')
        temp_db_context.create(source='youtube', source_id='2', title='Video 2')
        temp_db_context.create(source='youtube', source_id='3', title='Video 3')
        
        count_deleted = temp_db_context.clear_all()
        
        assert count_deleted == 3
        assert temp_db_context.count() == 0
    
    def test_context_manager(self):
        """Test database context manager."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as f:
            db_path = f.name
        
        try:
            with DBContext(db_path) as db:
                record = db.create(
                    source='youtube',
                    source_id='context_test',
                    title='Context Test'
                )
                assert record is not None
            
            # Verify data persisted after context exit
            db2 = DBContext(db_path)
            record = db2.read('youtube', 'context_test')
            assert record is not None
            db2.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)


class TestScoreDictionary:
    """Tests for score dictionary functionality."""
    
    def test_set_and_get_score_dict(self, temp_db_context):
        """Test setting and getting score dictionary."""
        score_dict = {
            'engagement_rate': 0.85,
            'views': 10000,
            'likes': 500,
            'comments': 50
        }
        
        record = temp_db_context.create(
            source='youtube',
            source_id='score_dict_test',
            title='Score Dict Test'
        )
        
        record.set_score_dict(score_dict)
        retrieved_dict = record.get_score_dict()
        
        assert retrieved_dict == score_dict
    
    def test_score_dict_with_upsert(self, temp_db_context):
        """Test score dictionary with upsert operation."""
        initial_dict = {'views': 1000}
        updated_dict = {'views': 2000, 'likes': 100}
        
        # Create with initial score dict
        temp_db_context.upsert(
            source='youtube',
            source_id='upsert_score',
            title='Test',
            score_dictionary=initial_dict
        )
        
        # Update with new score dict
        record = temp_db_context.upsert(
            source='youtube',
            source_id='upsert_score',
            title='Test',
            score_dictionary=updated_dict
        )
        
        assert record.get_score_dict() == updated_dict


class TestProcessedField:
    """Tests for the processed field."""
    
    def test_processed_field_defaults_to_false(self, temp_db_context):
        """Test that processed field defaults to False on creation."""
        record = temp_db_context.create(
            source='youtube',
            source_id='test_processed_1',
            title='Test Processed Field'
        )
        
        assert record is not None
        assert record.processed is False
    
    def test_processed_field_in_to_dict(self, temp_db_context):
        """Test that processed field is included in to_dict output."""
        record = temp_db_context.create(
            source='youtube',
            source_id='test_processed_2',
            title='Test Processed Dict'
        )
        
        record_dict = record.to_dict()
        assert 'processed' in record_dict
        assert record_dict['processed'] is False
    
    def test_update_processed_field(self, temp_db_context):
        """Test updating the processed field."""
        # Create record
        record = temp_db_context.create(
            source='youtube',
            source_id='test_processed_3',
            title='Test Update Processed'
        )
        
        assert record.processed is False
        
        # Update processed field
        updated_record = temp_db_context.update(
            source='youtube',
            source_id='test_processed_3',
            processed=True
        )
        
        assert updated_record is not None
        assert updated_record.processed is True
