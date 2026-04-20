# Technical Documentation

Welcome to the technical documentation for forschung.stadtgeschichtebasel.ch. This section contains detailed information for developers and contributors.

## 📚 Getting Started

- **[Setup Guide](../SETUP.md)** - Complete setup instructions for new contributors
- **[Contributing Guide](../CONTRIBUTING.md)** - Guidelines for contributing to the project
- **[Troubleshooting Guide](../TROUBLESHOOTING.md)** - Solutions to common problems
- **[API Documentation](../API.md)** - API reference and integration guide

## 🔧 Setup and Configuration

### Initial Setup

- [metadata.md](metadata.md) - Understanding and working with metadata
- [metadata-template.csv](metadata-template.csv) - Template for metadata structure
- [rake_tasks.md](rake_tasks.md) - Available Rake tasks for builds and deployment

### Migration and Upgrades

- [migrate_to_sa.md](migrate_to_sa.md) - Migration guide for standalone versions

## 🚀 Deployment and Building

- [build.md](build.md) - Build process and optimization
- [analytics.md](analytics.md) - Analytics integration
- [cloud.md](cloud.md) - Cloud deployment options

## 🎨 Theme and Customization

### Visual Customization

- [advanced_theme.md](advanced_theme.md) - Advanced theming options
- [color_theme.md](color_theme.md) - Customizing colors and branding

### Localization

- [localization.md](localization.md) - Multi-language support (German, Spanish, English)

## 📄 Page Components and Features

### Core Pages

- [item_pages.md](item_pages.md) - Item detail pages and display templates
- [data.md](data.md) - Data visualization page
- [navbar.md](navbar.md) - Navigation bar configuration

### Visualizations

- [maps.md](maps.md) - Geographic visualization with Leaflet
- [cloud.md](cloud.md) - Word cloud and subject visualization
- [list.md](list.md) - List visualization with frequencies
- [tables.md](tables.md) - Interactive table displays
- [compound_objects.md](compound_objects.md) - Handling multi-part objects

## 🛠 Technical Components

### Core Functionality

- [plugins.md](plugins.md) - Jekyll plugins and custom functionality
- [code_design_notes.md](code_design_notes.md) - Architecture and design decisions
- [markup.md](markup.md) - HTML and semantic markup

### Media and Assets

- [icons.md](icons.md) - Icon system and customization
- [gallery.md](gallery.md) - Image gallery (Spotlight)
- [lazyload.md](lazyload.md) - Lazy loading implementation for performance
- [foot.md](foot.md) - Footer and script loading

### Integrations and APIs

- [oai-pmh.md](oai-pmh.md) - OAI-PMH metadata harvesting endpoint
- [youtube.md](youtube.md) - YouTube integration recipes
- [noindex.md](noindex.md) - Search engine indexing control

## 🔗 External Resources

- [CollectionBuilder Documentation](https://collectionbuilder.github.io/cb-docs/) - Main CollectionBuilder docs
- [Jekyll Documentation](https://jekyllrb.com/docs/) - Jekyll static site generator
- [Bootstrap Documentation](https://getbootstrap.com/docs/) - Frontend framework
- [Neurodiversity Design System](https://neurodiversity.design/) - Inclusive design principles

## 📊 Stadt.Geschichte.Basel Extensions

This platform extends CollectionBuilder with several custom features:

1. **List Visualization** - Field visualization with frequencies
2. **EDTF Timeline** - Extended Date/Time Format support
3. **Geodata Layout** - Interactive GeoJSON map display
4. **Table Layout** - CSV data as interactive tables
5. **Multi-Language Support** - German, Spanish, English
6. **Trigger Warning** - Content warning system
7. **Report Button** - Data quality feedback mechanism
8. **GitHub Actions** - Automated builds and data processing
9. **Prettier Integration** - Code formatting

See the [main README](../README.md#project-specific-extensions-to-collectionbuilder) for details.

## 🤝 Contributing to Documentation

Found an error or want to improve the docs?

1. Read the [Contributing Guide](../CONTRIBUTING.md)
2. Edit the relevant `.md` file
3. Submit a pull request

## 💬 Get Help

- **Questions**: [GitHub Discussions](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/issues)
- **Troubleshooting**: [Troubleshooting Guide](../TROUBLESHOOTING.md)

---

**Note**: This documentation is for CollectionBuilder-CSV as extended by Stadt.Geschichte.Basel. For the base CollectionBuilder documentation, see [CB-Docs](https://collectionbuilder.github.io/cb-docs/).
