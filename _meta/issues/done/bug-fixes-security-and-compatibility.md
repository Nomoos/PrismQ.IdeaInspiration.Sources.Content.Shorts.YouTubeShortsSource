# Bug Fixes: Security and Compatibility Issues

## Description
This issue tracks multiple bugs identified and fixed in the PrismQ.IdeaCollector codebase related to security, compatibility, and robustness.

## Bugs Fixed

### 1. SQL Injection Vulnerability in Database Layer

**Severity**: Medium  
**File**: `src/database.py`

**Problem**: The `get_all_ideas()` method used string formatting for the `order_by` parameter, which could potentially be exploited for SQL injection attacks.

**Solution**: Added input validation that:
- Validates column names against an allowlist
- Validates sort directions (ASC/DESC)
- Provides safe defaults for invalid input
- Raises ValueError for malicious inputs

**Impact**: Prevents potential SQL injection attacks and improves code security.

### 2. Batch File Syntax Error in Windows Scripts

**Severity**: Low  
**File**: `scripts/quickstart.bat`

**Problem**: Used `else if` syntax which is not standard in Windows batch files and may fail in some environments.

**Solution**: Converted to proper nested `if-else` structure with correct parentheses placement.

**Impact**: Ensures compatibility with all Windows CMD versions.

### 3. Special Character Handling in Shell Scripts

**Severity**: Medium  
**Files**: 
- `scripts/setup.sh`
- `scripts/quickstart.sh`
- `scripts/setup.bat`
- `scripts/quickstart.bat`

**Problem**: API keys containing special characters (e.g., `&`, `/`, `\`) could break sed/PowerShell replacement commands.

**Solution**: 
- **Shell scripts**: Added character escaping before sed replacement
- **Batch scripts**: Improved PowerShell variable handling to prevent injection

**Impact**: Robust handling of API keys with special characters.

### 4. Missing .gitignore Entry

**Severity**: Low  
**File**: `.gitignore`

**Problem**: Backup files (`.env.bak`) created by sed commands were not ignored by git.

**Solution**: Added `.env.bak` to `.gitignore`.

**Impact**: Prevents accidental commit of backup configuration files.

## Testing

### New Tests Added
Created comprehensive security test suite in `tests/test_database_security.py`:
- `test_order_by_validation`: Validates proper input handling
- `test_sql_injection_prevention`: Ensures SQL injection is blocked
- `test_limit_validation`: Validates limit parameter
- `test_order_by_edge_cases`: Tests edge cases and defaults

### Test Results
- All 32 existing tests: ✅ PASS
- All 4 new security tests: ✅ PASS
- **Total: 36/36 tests passing**

## Files Changed
1. `src/database.py` - Added input validation for SQL parameters
2. `scripts/quickstart.bat` - Fixed batch file syntax
3. `scripts/setup.bat` - Improved PowerShell string handling
4. `scripts/quickstart.sh` - Added character escaping for sed
5. `scripts/setup.sh` - Added character escaping for sed
6. `.gitignore` - Added `.env.bak` entry
7. `tests/test_database_security.py` - New security test suite

## Verification Steps

1. Run all tests: `pytest -v`
2. Check shell script syntax: `bash -n scripts/*.sh`
3. Test CLI commands: `python -m src.cli --help`
4. Verify malicious inputs are rejected (see security tests)

## Related Issues
None

## Links
- Commit: [See PR]
- Tests: `tests/test_database_security.py`

## Notes
- All changes maintain backward compatibility
- No breaking changes to existing APIs
- Security improvements follow OWASP best practices
