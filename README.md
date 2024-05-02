# forschung.stadtgeschichtebasel.ch

The open-source code of the digital platform for research data of Stadt.Geschichte.Basel.

[![GitHub issues](https://img.shields.io/github/issues/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch.svg)](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/issues)
[![GitHub forks](https://img.shields.io/github/forks/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch.svg)](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/network)
[![GitHub stars](https://img.shields.io/github/stars/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch.svg)](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/stargazers)
[![GitHub license](https://img.shields.io/github/license/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch.svg)](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/blob/main/LICENSE.md)

## Overview

Welcome to [Stadt.Geschichte.Basel](https://stadtgeschichtebasel.ch/), a historical research project at the University of Basel in Switzerland, funded with over 9 million Swiss Francs from public and private sources, running from 2017 to 2025. It is a comprehensive digital and print project that aims to present the multifaceted history of Basel from its earliest beginnings to the present day. Visit [Stadt.Geschichte.Basel](https://stadtgeschichtebasel.ch) to see how our digital portal brings Basel's history to life.

[Stadt.Geschichte.Basel](https://stadtgeschichtebasel.ch/) seeks to bridge research gaps and present historical findings in accessible formats. Our project encompasses an [extensive nine-volume book series](https://www.merianverlag.ch/buecher/stadt.geschichte.basel.html), an overview volume, a digital portal, and a digital platform for research data. Hosted at the University of Basel, this project aims to make historical research and insights accessible to scholars and the public like never before.

This project is the open-source code of the digital platform for research data of Stadt.Geschichte.Basel. It is a static website built with [CollectionBuilder-CSV](https://collectionbuilder.github.io/) and hosted on [GitHub Pages](https://pages.github.com/). The research data collection itself is hosted at the University of Bern's [instance of Omeka S](https://omeka.unibe.ch/s/stadtgeschichtebasel/page/sgb).

## Key Features

- **Fast Static Website**: Built with CollectionBuilder-CSV using open source static site generator [Jekyll](https://jekyllrb.com/) and a modern static web stack.
- **Explorative Access to Metadata**: Interactive features for exploring collection metadata such as a timeline, filtering and comprehensive annotation.
- **Sensitive Content Annotation**: Collection items are annotated using the [GenderOpen Index](https://opengenderplatform.de/schlagwortindex), a controlled vocabulary for sensitive content.
- **Accessibility-Focused Design**: Ensuring inclusivity for all users by complying with WCAG standards and observing neurodiversity design guidelines. More at our [accessibility statement](https://stadtgeschichtebasel.ch/barrierefreiheitserklaerung/).

### CollectionBuilder 

CollectionBuilder, an open source framework for creating metadata-driven digital collections, is the foundation of Stadt.Geschichte.Basel's research data platform. CollectionBuilder is a project maintained by the University of Idaho Library's [Digital Initiatives](https://www.lib.uidaho.edu/digital/) and the [Center for Digital Inquiry and Learning](https://cdil.lib.uidaho.edu) (CDIL) following the [Lib-Static](https://lib-static.github.io/) methodology. 

The basic theme is created using [Bootstrap](https://getbootstrap.com/).
Metadata visualizations are built using open source libraries such as [DataTables](https://datatables.net/), [Spotlight gallery](https://github.com/nextapps-de/spotlight), [lazysizes](https://github.com/aFarkas/lazysizes), and [Lunr.js](https://lunrjs.com/).
Object metadata is exposed using [Schema.org](http://schema.org) and [Open Graph protocol](http://ogp.me/) standards.

For more information on CollectionBuilder, visit the [Docs](https://collectionbuilder.github.io/cb-docs/).

## Data Model

**todo** mermaid

## Installation

Use [Bundle](https://bundler.io/) to install all dependencies.

```bash
bundle install
```

## Usage

Run the development server.

```bash
bundle exec jekyll serve
```

Build for production.

```bash
rake deploy
```

## Support

This project is maintained by [@Stadt-Geschichte-Basel](https://github.com/Stadt-Geschichte-Basel). Please understand that we won't be able to provide individual support via email. We believe that help is much more valuable if it's shared publicly, so that more people can benefit from it.

| Type                                   | Platforms                                                                                           |
| -------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 🚨 **Bug Reports**                     | [GitHub Issue Tracker](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/issues)    |
| 🎁 **Feature Requests**                | [GitHub Issue Tracker](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/issues)    |
| 🛡 **Report a security vulnerability** | [GitHub Issue Tracker](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/issues)    |
| 💬 **General Questions**               | [GitHub Discussions](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/discussions) |

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/tags).

## Authors and acknowledgment

- **Moritz Mähr** - [maehr](https://github.com/maehr)
- **Nico Görlich** - [koilebeit](https://github.com/koilebeit)
- **Moritz Twente** - [mtwente](https://github.com/mtwente)

See also the list of [contributors](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/graphs/contributors) who participated in this project.

----------

## License

CollectionBuilder documentation and general web content is licensed [Creative Commons Attribution-ShareAlike 4.0 International](http://creativecommons.org/licenses/by-sa/4.0/). 
This license does *NOT* include any objects or images used in digital collections, which may have individually applied licenses described by a "rights" field.
CollectionBuilder code is licensed [MIT](https://github.com/CollectionBuilder/collectionbuilder-csv/blob/master/LICENSE). 
This license does not include external dependencies included in the `assets/lib` directory, which are covered by their individual licenses.
