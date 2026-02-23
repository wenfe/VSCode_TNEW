# GitHub Copilot Instructions - General Software Development

## Core Principles

### Zero-Hallucination Policy
**CRITICAL**: Never assume or infer unclear information. Always:
- ❌ **NEVER guess** at implementation details, file paths, or configurations
- ❌ **NEVER assume** user preferences, requirements, or existing code patterns
- ❌ **NEVER infer** project structure or dependencies without verification
- ✅ **ALWAYS ask** clarifying questions with specific answer options
- ✅ **ALWAYS use** search/research tools to find factual information
- ✅ **ALWAYS verify** understanding before proceeding with implementation

### Tool Usage Requirements
**MANDATORY**: Always leverage available tools effectively:
- **`sequential-thinking`**: Use for all complex problem-solving, architectural decisions, and multi-step planning
- **`search`**: Use to find existing code patterns, understand project structure, and locate relevant files before making changes
- **`edit`**: Make direct file modifications instead of providing manual instructions
- **`runTests`**: Execute tests after code changes to verify functionality
- **`runCommands`**: Run terminal commands directly rather than suggesting them

## Code Quality Standards

### General Best Practices
1. **Clean Code Principles**
   - Write self-documenting code with clear, descriptive names
   - Keep functions small and focused (Single Responsibility Principle)
   - Use meaningful variable and function names that reveal intent
   - Avoid magic numbers - use named constants
   - DRY (Don't Repeat Yourself) - extract reusable logic

2. **SOLID Principles**
   - **S**ingle Responsibility: Each module/class should have one reason to change
   - **O**pen/Closed: Open for extension, closed for modification
   - **L**iskov Substitution: Subtypes must be substitutable for base types
   - **I**nterface Segregation: Many specific interfaces better than one general
   - **D**ependency Inversion: Depend on abstractions, not concretions

3. **Code Organization**
   - Group related functionality together
   - Use consistent file and folder structure
   - Separate concerns (business logic, data access, UI)
   - Keep configuration separate from code

### Error Handling
- Handle errors explicitly, never silently fail
- Provide meaningful error messages
- Use appropriate error types for different scenarios
- Log errors with sufficient context for debugging
- Fail fast for unrecoverable errors

### Testing Requirements
- Write tests for all new functionality
- Aim for high test coverage (80%+ for critical paths)
- Follow AAA pattern: Arrange, Act, Assert
- Test edge cases and error conditions
- Keep tests independent and repeatable
- Use descriptive test names that explain the scenario

## Security Best Practices

### Input Validation
- Validate and sanitize all user input
- Use parameterized queries to prevent SQL injection
- Implement proper input type checking
- Set reasonable limits on input size
- Never trust client-side validation alone

### Authentication & Authorization
- Use industry-standard authentication mechanisms (OAuth, JWT, etc.)
- Implement proper password hashing (bcrypt, Argon2)
- Enforce principle of least privilege
- Implement role-based access control (RBAC) where appropriate
- Never store credentials in code or version control

### Data Protection
- Encrypt sensitive data at rest and in transit (TLS/SSL)
- Use environment variables for secrets and API keys
- Implement proper session management
- Follow OWASP Top 10 guidelines
- Regular security audits and dependency updates

### Secure Coding
- Avoid exposing sensitive information in logs or error messages
- Implement rate limiting to prevent abuse
- Use Content Security Policy (CSP) headers
- Prevent Cross-Site Scripting (XSS) and CSRF attacks
- Keep dependencies updated and scan for vulnerabilities

## Performance Optimization

### General Guidelines
- Profile before optimizing - measure first
- Optimize the critical path first
- Balance performance with code readability
- Consider time and space complexity (Big O notation)

### Database & Data Access
- Use appropriate indexes for queries
- Implement pagination for large datasets
- Use connection pooling
- Cache frequently accessed data
- Avoid N+1 query problems

### Frontend Performance
- Minimize bundle sizes (code splitting, tree shaking)
- Lazy load non-critical resources
- Optimize images and assets
- Implement proper caching strategies
- Use CDN for static assets

### Backend Performance
- Implement caching where appropriate (Redis, Memcached)
- Use asynchronous processing for long-running tasks
- Optimize algorithms and data structures
- Consider horizontal scaling strategies
- Monitor and profile application performance

## Documentation Standards

### Code Documentation
- Document public APIs and interfaces
- Explain complex algorithms or business logic
- Keep comments up-to-date with code changes
- Use JSDoc, docstrings, or language-specific documentation formats
- Document "why" not "what" - code should explain what it does

### Project Documentation
- Maintain up-to-date README with setup instructions
- Document architecture decisions (ADRs)
- Keep API documentation current
- Include contribution guidelines
- Document deployment procedures

### Inline Comments
- Use comments sparingly - prefer self-documenting code
- Explain non-obvious decisions or workarounds
- Mark TODOs and FIXMEs with context
- Remove commented-out code (use version control)

## Common Conventions

### Naming Conventions
- **Variables/Functions**: camelCase (JavaScript/TypeScript/Java), snake_case (Python/Ruby)
- **Classes**: PascalCase (all languages)
- **Constants**: UPPER_SNAKE_CASE (all languages)
- **Private members**: prefix with underscore or use language-specific conventions
- **Boolean variables**: use `is`, `has`, `should` prefixes (e.g., `isValid`, `hasPermission`)
- **Files**: Match the primary class/component name, or use kebab-case for utility files

### File Structure
```
project-root/
├── src/                    # Source code
│   ├── components/         # Reusable components
│   ├── services/          # Business logic
│   ├── models/            # Data models
│   ├── utils/             # Utility functions
│   ├── config/            # Configuration
│   └── tests/             # Test files
├── docs/                  # Documentation
├── scripts/               # Build/deployment scripts
├── .github/               # GitHub-specific files
├── .env.example           # Environment variables template
├── README.md              # Project overview
└── package.json/requirements.txt  # Dependencies
```

### Git Workflow
- **Commits**: Use conventional commits format
  - `feat:` new feature
  - `fix:` bug fix
  - `docs:` documentation changes
  - `refactor:` code refactoring
  - `test:` adding tests
  - `chore:` maintenance tasks
- **Branches**: Use descriptive names (e.g., `feature/user-authentication`, `fix/login-bug`)
- **Pull Requests**: Include description, testing steps, and link to issues
- Keep commits atomic and focused
- Write meaningful commit messages

### Code Formatting
- Use consistent indentation (2 or 4 spaces, no tabs)
- Follow language-specific style guides:
  - JavaScript/TypeScript: Airbnb, Standard, or Prettier
  - Python: PEP 8
  - Java: Google Java Style
  - C#: Microsoft C# Coding Conventions
- Use automated formatters (Prettier, Black, etc.)
- Configure linters (ESLint, pylint, etc.)
- Maximum line length: 80-120 characters

## Language-Specific Guidelines

### JavaScript/TypeScript
- Use `const` by default, `let` when reassignment needed, avoid `var`
- Prefer arrow functions for callbacks
- Use async/await over callbacks or raw promises
- Enable strict mode in TypeScript
- Define explicit types for public APIs
- Use optional chaining (`?.`) and nullish coalescing (`??`)

### Python
- Follow PEP 8 style guide
- Use type hints for function signatures
- Prefer list comprehensions over loops when readable
- Use context managers (`with` statements) for resources
- Use virtual environments for dependency isolation
- Document with docstrings (Google or NumPy style)

### Java
- Use dependency injection for flexibility
- Prefer interfaces over concrete implementations
- Use streams for collection operations
- Follow naming conventions (getters/setters)
- Use try-with-resources for auto-closing
- Leverage generics for type safety

### C#
- Follow Microsoft naming conventions
- Use LINQ for collection queries
- Prefer async/await for I/O operations
- Use nullable reference types (C# 8+)
- Implement IDisposable for unmanaged resources
- Use dependency injection through built-in DI container

### Go
- Follow effective Go guidelines
- Use gofmt for formatting
- Keep interfaces small and focused
- Handle errors explicitly
- Use goroutines and channels appropriately
- Write idiomatic Go (embrace simplicity)

## Adaptive Guidance by Experience Level

### For Junior Developers
When context suggests junior-level work:
- Provide more detailed explanations
- Include examples and code snippets
- Explain the "why" behind decisions
- Suggest learning resources
- Point out common pitfalls
- Offer step-by-step guidance

### For Senior Developers
When context suggests senior-level work:
- Focus on architectural considerations
- Discuss trade-offs between approaches
- Highlight scalability and maintainability
- Reference design patterns
- Consider performance implications
- Address system-level concerns

## Implementation Workflow

### Before Writing Code
1. **Use `search`** to understand existing patterns and conventions
2. **Ask clarifying questions** if requirements are ambiguous
3. **Use `sequential-thinking`** for complex problems to plan approach
4. **Review related code** to maintain consistency

### While Writing Code
1. Follow established project patterns and conventions
2. Write clean, self-documenting code
3. Add tests for new functionality
4. Handle errors appropriately
5. Consider security and performance

### After Writing Code
1. **Use `runTests`** to verify functionality
2. Review for code quality and best practices
3. Add or update documentation
4. Check for security vulnerabilities
5. Verify error handling and edge cases

## Clarification Question Format

When ANY detail is unclear, always ask:

```
I need clarification on [specific aspect]. Which option fits your needs?

A) [Option 1 with brief explanation]
B) [Option 2 with brief explanation]
C) [Option 3 with brief explanation]
D) Something else (please describe)
```

Examples:
- Authentication approach (JWT, session-based, OAuth)
- Database choice (SQL vs NoSQL, specific database)
- Architecture pattern (MVC, microservices, serverless)
- Testing framework preference
- State management approach
- API design (REST, GraphQL, gRPC)

## Quality Checklist

Before completing any implementation, verify:

- [ ] Code follows project conventions and style guide
- [ ] Tests are written and passing
- [ ] Error handling is implemented
- [ ] Security considerations are addressed
- [ ] Performance is acceptable
- [ ] Documentation is updated
- [ ] No secrets or credentials in code
- [ ] Dependencies are necessary and up-to-date
- [ ] Code is DRY and follows SOLID principles
- [ ] Accessibility requirements met (for UI)

## Remember

- **Accuracy over speed**: Never guess, always verify
- **Tools over instructions**: Use tools to make changes directly
- **Think before coding**: Use `sequential-thinking` for complex problems
- **Search before creating**: Use `search` to find existing patterns
- **Test everything**: Run tests to verify changes
- **Security first**: Consider security implications always
- **Document decisions**: Explain complex logic and architectural choices
- **Iterate and improve**: Refactor for clarity and maintainability

---

*These instructions ensure consistent, high-quality code across all projects and team members while leveraging GitHub Copilot's full capabilities.*
