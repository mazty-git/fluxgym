# UI Assets

This directory contains extracted UI assets for FluxGym, separated from the main application logic for better maintainability.

## Files

### `styles.css`
Custom CSS styles for the Gradio interface including:
- Navigation bar styling
- Training terminal appearance
- Caption container with scrollable layout for large datasets
- Toast notification styling
- Button states and animations
- Responsive layout helpers

### `scripts.js`
Client-side JavaScript functionality including:
- **Autoscroll**: Automatically scrolls the training log output
- **Debounced Refresh**: Prevents excessive updates when form inputs change
- **Training Button State**: Updates button appearance when training starts

## Architecture

The UI assets are loaded dynamically by `app.py` using the `load_css()` and `load_js()` helper functions. This approach:

1. **Separates Concerns**: UI styling separate from Python business logic
2. **Improves Readability**: No more multi-line string literals in Python
3. **Better IDE Support**: Proper syntax highlighting and linting for CSS/JS
4. **Easier Maintenance**: Changes to styles don't require Python knowledge
5. **Future Extensibility**: Easy to add more UI assets as needed

## Usage

The files are automatically loaded when the application starts. No manual intervention required.

If you modify these files, simply restart the application to see changes.

## Future Plans

As this refactoring continues, this directory may include:
- `components.py` - Reusable Gradio component definitions
- `layout.py` - Main UI layout separated from app logic
- Additional theme files or variants
