"""Tests for the YouTubeVideo model and DBContext."""

import pytest
import tempfile
import os
from Model import YouTubeVideo, DBContext


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


@pytest.fixture
def sample_ytdlp_data():
    """Sample yt-dlp data for testing."""
    return {
        'id': 'test_video_123',
        'title': 'Test Video Title',
        'description': 'Test description',
        'uploader': 'Test Channel',
        'uploader_id': 'test_channel_id',
        'channel': 'Test Channel',
        'channel_id': 'UCtest123',
        'duration': 45,
        'view_count': 10000,
        'like_count': 500,
        'comment_count': 50,
        'thumbnail': 'https://example.com/thumb.jpg',
        'upload_date': '20250119',
        'timestamp': 1642550400,
        'tags': ['tag1', 'tag2'],
        'categories': ['Entertainment'],
        'width': 1080,
        'height': 1920,
        'fps': 30,
    }


class TestYouTubeVideoModel:
    """Tests for the YouTubeVideo model."""
    
    def test_model_creation(self, temp_db_context, sample_ytdlp_data):
        """Test creating a model instance."""
        record = temp_db_context.create('test123', sample_ytdlp_data)
        
        assert record is not None
        assert record.video_id == 'test123'
        assert record.get_field('title') == 'Test Video Title'
        assert record.get_field('view_count') == 10000
    
    def test_model_raw_data(self, temp_db_context, sample_ytdlp_data):
        """Test raw data storage."""
        record = temp_db_context.create('test456', sample_ytdlp_data)
        
        assert record is not None
        raw_data = record.get_raw_data()
        assert raw_data == sample_ytdlp_data
        assert raw_data['title'] == 'Test Video Title'
        assert raw_data['view_count'] == 10000
    
    def test_model_to_dict(self, temp_db_context, sample_ytdlp_data):
        """Test converting model to dictionary."""
        record = temp_db_context.create('test789', sample_ytdlp_data)
        
        record_dict = record.to_dict()
        assert record_dict['video_id'] == 'test789'
        assert 'raw_data' in record_dict
        assert 'created_at' in record_dict
        assert 'updated_at' in record_dict
    
    def test_model_get_field(self, temp_db_context, sample_ytdlp_data):
        """Test get_field method."""
        record = temp_db_context.create('test_field', sample_ytdlp_data)
        
        assert record.get_field('title') == 'Test Video Title'
        assert record.get_field('view_count') == 10000
        assert record.get_field('nonexistent', 'default') == 'default'
    
    def test_model_repr(self, temp_db_context, sample_ytdlp_data):
        """Test model string representation."""
        record = temp_db_context.create('test_repr', sample_ytdlp_data)
        
        repr_str = repr(record)
        assert 'YouTubeVideo' in repr_str
        assert 'test_repr' in repr_str


class TestDBContextCRUD:
    """Tests for DBContext CRUD operations."""
    
    def test_create(self, temp_db_context, sample_ytdlp_data):
        """Test create operation."""
        record = temp_db_context.create('create_test', sample_ytdlp_data)
        
        assert record is not None
        assert record.id is not None
        assert record.video_id == 'create_test'
    
    def test_create_duplicate(self, temp_db_context, sample_ytdlp_data):
        """Test that creating duplicate records fails."""
        temp_db_context.create('duplicate', sample_ytdlp_data)
        
        # Try to create duplicate
        duplicate = temp_db_context.create('duplicate', sample_ytdlp_data)
        
        assert duplicate is None
    
    def test_read(self, temp_db_context, sample_ytdlp_data):
        """Test read operation."""
        created = temp_db_context.create('read_test', sample_ytdlp_data)
        
        retrieved = temp_db_context.read('read_test')
        
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.get_field('title') == 'Test Video Title'
    
    def test_read_nonexistent(self, temp_db_context):
        """Test reading non-existent record."""
        record = temp_db_context.read('nonexistent')
        assert record is None
    
    def test_read_by_id(self, temp_db_context, sample_ytdlp_data):
        """Test read by ID operation."""
        created = temp_db_context.create('id_test', sample_ytdlp_data)
        
        retrieved = temp_db_context.read_by_id(created.id)
        
        assert retrieved is not None
        assert retrieved.video_id == 'id_test'
    
    def test_update(self, temp_db_context, sample_ytdlp_data):
        """Test update operation."""
        temp_db_context.create('update_test', sample_ytdlp_data)
        
        updated_data = sample_ytdlp_data.copy()
        updated_data['title'] = 'Updated Title'
        updated_data['view_count'] = 20000
        
        updated = temp_db_context.update('update_test', updated_data)
        
        assert updated is not None
        assert updated.get_field('title') == 'Updated Title'
        assert updated.get_field('view_count') == 20000
    
    def test_update_nonexistent(self, temp_db_context, sample_ytdlp_data):
        """Test updating non-existent record."""
        result = temp_db_context.update('nonexistent', sample_ytdlp_data)
        
        assert result is None
    
    def test_upsert_create(self, temp_db_context, sample_ytdlp_data):
        """Test upsert creating a new record."""
        record = temp_db_context.upsert('upsert_new', sample_ytdlp_data)
        
        assert record is not None
        assert record.get_field('title') == 'Test Video Title'
    
    def test_upsert_update(self, temp_db_context, sample_ytdlp_data):
        """Test upsert updating an existing record."""
        temp_db_context.create('upsert_existing', sample_ytdlp_data)
        
        updated_data = sample_ytdlp_data.copy()
        updated_data['title'] = 'Updated Title'
        
        updated = temp_db_context.upsert('upsert_existing', updated_data)
        
        assert updated is not None
        assert updated.get_field('title') == 'Updated Title'
        
        # Verify only one record exists
        count = temp_db_context.count()
        assert count == 1
    
    def test_delete(self, temp_db_context, sample_ytdlp_data):
        """Test delete operation."""
        temp_db_context.create('delete_test', sample_ytdlp_data)
        
        result = temp_db_context.delete('delete_test')
        assert result is True
        
        # Verify deletion
        record = temp_db_context.read('delete_test')
        assert record is None
    
    def test_delete_nonexistent(self, temp_db_context):
        """Test deleting non-existent record."""
        result = temp_db_context.delete('nonexistent')
        assert result is False
    
    def test_list_all(self, temp_db_context, sample_ytdlp_data):
        """Test listing all records."""
        data1 = sample_ytdlp_data.copy()
        data2 = sample_ytdlp_data.copy()
        data3 = sample_ytdlp_data.copy()
        
        temp_db_context.create('video1', data1)
        temp_db_context.create('video2', data2)
        temp_db_context.create('video3', data3)
        
        records = temp_db_context.list_all()
        
        assert len(records) == 3
    
    def test_list_all_with_limit(self, temp_db_context, sample_ytdlp_data):
        """Test listing records with limit."""
        for i in range(10):
            data = sample_ytdlp_data.copy()
            temp_db_context.create(f'video_{i}', data)
        
        records = temp_db_context.list_all(limit=5)
        assert len(records) == 5
    
    def test_count(self, temp_db_context, sample_ytdlp_data):
        """Test count operation."""
        assert temp_db_context.count() == 0
        
        temp_db_context.create('video1', sample_ytdlp_data)
        temp_db_context.create('video2', sample_ytdlp_data.copy())
        
        assert temp_db_context.count() == 2
    
    def test_clear_all(self, temp_db_context, sample_ytdlp_data):
        """Test clearing all records."""
        temp_db_context.create('video1', sample_ytdlp_data)
        data2 = sample_ytdlp_data.copy()
        temp_db_context.create('video2', data2)
        
        count_deleted = temp_db_context.clear_all()
        
        assert count_deleted == 2
        assert temp_db_context.count() == 0
    
    def test_context_manager(self, sample_ytdlp_data):
        """Test database context manager."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as f:
            db_path = f.name
        
        try:
            with DBContext(db_path) as db:
                record = db.create('context_test', sample_ytdlp_data)
                assert record is not None
            
            # Verify data persisted after context exit
            db2 = DBContext(db_path)
            record = db2.read('context_test')
            assert record is not None
            db2.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
