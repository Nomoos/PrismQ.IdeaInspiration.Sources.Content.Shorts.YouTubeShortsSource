# Business/Domain Modules (`mod/`)

This directory contains business logic and domain-specific modules for the PrismQ application.

## Purpose

The `mod/` directory is designed to hold higher-level modules that implement:
- Business logic and domain models
- Use case implementations
- Domain-specific workflows
- Application-specific modules

## Separation of Concerns

The repository follows a clear separation:

- **`src/`** - Core Python package implementation
  - Configuration management (`config.py`)
  - Logging infrastructure (`logging_config.py`)
  - Core utilities and infrastructure code
  - Package initialization and common functionality

- **`mod/`** - Business/domain modules (this directory)
  - Domain-specific implementations
  - Business logic modules
  - Higher-level application components
  - Use case orchestration

## Structure

Each module in this directory should be self-contained and follow these guidelines:

```
mod/
├── README.md                 # This file
├── ModuleExample/           # Example domain module
│   ├── __init__.py
│   └── ... (module files)
└── YourModule/              # Your domain modules
    ├── __init__.py
    └── ... (module files)
```

## Guidelines

When creating new modules:

1. **Single Responsibility**: Each module should focus on a specific domain or business concern
2. **Dependency Injection**: Depend on `src/` infrastructure via interfaces/protocols
3. **Testing**: Add corresponding tests in `tests/mod/YourModule/`
4. **Documentation**: Document the module's purpose, inputs, and outputs
5. **SOLID Principles**: Follow SOLID design principles (see `.github/copilot-instructions.md`)

## Examples

The `ModuleExample/` directory serves as a template for creating new business modules. Feel free to rename or replace it with your actual domain modules.

## Related Documentation

- Main README: `/README.md`
- Contributing Guidelines: `/docs/CONTRIBUTING.md` (if exists)
- Copilot Instructions: `/.github/copilot-instructions.md`
