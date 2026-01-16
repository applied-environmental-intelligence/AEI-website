# Contributing to AEI Website

Thank you for your interest in contributing to the AEI Website project! This document provides guidelines and best practices for contributing.

## 🎯 Code of Conduct

- Be respectful and professional
- Focus on constructive feedback
- Help maintain a welcoming environment

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AEI-website.git
   cd AEI-website
   ```
3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r scripts/requirements.txt
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📋 Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] **Code changes are in `src/`**, not `dist/`
- [ ] **Build passes successfully**: `python build.py` exits without errors
- [ ] **Local preview works**: Site displays correctly at `http://localhost:8000`
- [ ] **HTML is valid**: No syntax errors or broken tags
- [ ] **Links work**: All internal and external links function correctly
- [ ] **Animations load**: GIFs display and animate properly
- [ ] **Responsive design**: Tested on different screen sizes
- [ ] **No console errors**: Browser console shows no JavaScript errors
- [ ] **Git history is clean**: Meaningful commit messages
- [ ] **`.gitignore` respected**: No `dist/`, `venv/`, or `__pycache__/` committed
- [ ] **Documentation updated**: README or guides updated if needed

## 🎨 Code Style

### HTML
- Use 2-space indentation
- Use semantic HTML elements (`<section>`, `<article>`, `<nav>`, etc.)
- Include `alt` attributes for images
- Use meaningful IDs and class names
- Keep inline scripts minimal; prefer external files for large scripts

### CSS
- Use 2-space indentation
- Group related properties
- Use CSS variables for repeated values (colors, spacing)
- Comment complex selectors
- Mobile-first approach for responsive design

### Python
- Follow [PEP 8](https://pep8.org/) style guide
- Use 4-space indentation
- Add docstrings to functions and classes
- Include type hints where appropriate
- Use meaningful variable names
- Add comments for complex logic

### Commit Messages
Use clear, descriptive commit messages:

```
Good:
- "Add YouTube embed support to documentation"
- "Fix cable animation rendering bug at high resolutions"
- "Update team member bios and photos"

Avoid:
- "fix bug"
- "update stuff"
- "changes"
```

## 🔧 Types of Contributions

### 🐛 Bug Fixes

1. **Create an issue** describing the bug (if one doesn't exist)
2. **Reference the issue** in your PR: "Fixes #123"
3. **Include steps to reproduce** in the issue description
4. **Test thoroughly** before submitting

### ✨ New Features

1. **Discuss first** by opening an issue to propose the feature
2. **Keep it minimal** - avoid adding heavy dependencies
3. **Update documentation** to explain the new feature
4. **Add examples** showing how to use it

### 📝 Documentation

- Fix typos, clarify instructions, add examples
- Update guides when adding features
- Keep language clear and concise
- Add screenshots or GIFs for visual steps

### 🎨 Design Improvements

- Ensure changes are accessible (WCAG AA compliance)
- Test on multiple browsers (Chrome, Firefox, Safari)
- Test on mobile devices
- Maintain consistent visual language
- Consider performance impacts (file sizes, animations)

## 🧪 Testing

### Manual Testing Checklist

Test your changes on:
- [ ] **Chrome** (latest)
- [ ] **Firefox** (latest)
- [ ] **Safari** (if on macOS)
- [ ] **Mobile browsers** (iOS Safari, Chrome Mobile)
- [ ] **Different screen sizes**: 320px, 768px, 1024px, 1920px

### Build Testing

```bash
# Clean build from scratch
rm -rf dist/
python build.py

# Verify output
ls -lh dist/animations/

# Test locally
python -m http.server --directory dist 8000
```

## 📦 Dependencies

### Adding New Python Dependencies

1. Add to `scripts/requirements.txt`:
   ```
   package-name>=minimum.version
   ```
2. Document why it's needed in your PR description
3. Keep dependencies minimal and well-maintained
4. Pin versions to avoid future breakage

### External Services

Avoid adding dependencies on external services unless absolutely necessary. The site should work offline except for:
- Form submission (FormSubmit.co)
- Analytics (Google Analytics)
- External content (YouTube embeds)

## 🚫 What Not to Do

- ❌ **Don't commit `dist/`** - It's generated and gitignored
- ❌ **Don't commit large binary files** - Use Git LFS if needed
- ❌ **Don't break existing functionality** - Test thoroughly
- ❌ **Don't add heavy frameworks** (React, Vue, Angular) - Keep it lightweight
- ❌ **Don't include proprietary or copyrighted content** without permission
- ❌ **Don't include personal credentials** or API keys

## 🔍 Code Review Process

1. **Automated checks** run on all PRs (build, lint, deploy preview)
2. **Manual review** by maintainers
3. **Feedback incorporation** - Address review comments
4. **Approval and merge** - Maintainers merge approved PRs

## 📬 Communication

- **Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

## 🎓 Learning Resources

### Web Development
- [MDN Web Docs](https://developer.mozilla.org/) - HTML, CSS, JavaScript
- [Web.dev](https://web.dev/) - Modern web best practices
- [Can I Use](https://caniuse.com/) - Browser compatibility

### Python
- [Python Documentation](https://docs.python.org/3/)
- [Real Python](https://realpython.com/) - Tutorials and guides
- [Pillow Documentation](https://pillow.readthedocs.io/)

### Git
- [GitHub Docs](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [Learn Git Branching](https://learngitbranching.js.org/)

## 🏆 Recognition

Contributors will be acknowledged in:
- Git commit history
- GitHub contributors page
- Release notes (for significant contributions)

Thank you for contributing to make the AEI website better! 🎉
