# Content Security Policy (CSP)

## Overview

Content Security Policy (CSP) is a security feature that helps prevent cross-site scripting (XSS) attacks and other code injection attacks by restricting which resources can be loaded by the browser.

This CollectionBuilder site includes configurable CSP support to enhance security while maintaining compatibility with external services commonly used in digital collections.

## Configuration

CSP is configured in `_data/theme.yml` under the "ADVANCED OPTIONS" section:

```yaml
# CONTENT SECURITY POLICY [optional!]
# CSP helps protect against XSS attacks and other code injection attacks
# Set to true to enable CSP with default secure settings
csp-enabled: true
```

### Default CSP Policy

When `csp-enabled: true`, the following default policy is applied:

- **default-src**: `'self'` - Only allow resources from the same origin by default
- **script-src**: `'self' 'unsafe-inline'` plus trusted external domains:
  - `https://plausible.io` (analytics)
  - `https://cdn.jsdelivr.net` (Bootstrap, Universal Viewer, Leaflet)
  - `https://ajax.googleapis.com` (Model Viewer)
  - `https://cdn.knightlab.com` (TimelineJS)
  - `https://www.googletagmanager.com` (Google Analytics, if configured)
- **style-src**: `'self' 'unsafe-inline'` plus:
  - `https://cdn.jsdelivr.net` (Bootstrap)
  - `https://cdn.knightlab.com` (TimelineJS)
- **img-src**: `'self' data: https: http:` - Allow images from anywhere (common for digital collections)
- **font-src**: `'self' data:` - Allow self-hosted and data URI fonts
- **connect-src**: `'self' https://plausible.io` - Allow connections for analytics
- **frame-src**: `'self'` plus:
  - `https://player.vimeo.com` (video embeds)
  - `https://www.youtube-nocookie.com` (YouTube embeds)
- **object-src**: `'none'` - Block object/embed/applet elements for security
- **base-uri**: `'self'` - Prevent base tag hijacking

### Custom CSP Policy

For advanced users, you can override the default policy by uncommenting and customizing the `csp-directives` option:

```yaml
# Override default CSP directives (advanced users only)
csp-directives:
  default-src: "'self'"
  script-src: "'self' 'unsafe-inline' https://example.com"
  style-src: "'self' 'unsafe-inline'"
  # ... additional directives
```

## Security Considerations

### Why `'unsafe-inline'`?

The policy includes `'unsafe-inline'` for scripts and styles because:

1. **CollectionBuilder compatibility**: The framework includes inline styles and scripts
2. **Jekyll template variables**: Dynamic content generation requires inline scripts
3. **Practicality**: Eliminating all inline code would require significant refactoring

### Alternative to Integrity Attributes

CSP provides a more maintainable security approach compared to integrity attributes because:

- **No hash maintenance**: External scripts can update without breaking the site
- **Broader protection**: Protects against various attack vectors, not just script tampering
- **Domain-based trust**: Allows all scripts from trusted domains

## Implementation Details

CSP is implemented through:

1. **Configuration**: `_data/theme.yml` provides the enable/disable switch and custom directives
2. **Template**: `_includes/head/csp.html` generates the CSP meta tag based on configuration
3. **Integration**: `_includes/head/head.html` includes the CSP template early in the `<head>` section

The CSP meta tag is only included when `csp-enabled: true` in the theme configuration.

## Testing

To verify CSP is working:

1. Build the site with `JEKYLL_ENV=production bundle exec jekyll build`
2. Check the generated HTML for the CSP meta tag in the `<head>` section
3. Use browser developer tools to verify the policy is applied
4. Monitor console for any CSP violations

## Troubleshooting

If you encounter CSP violations:

1. **Check browser console**: Look for CSP violation errors
2. **Identify blocked resources**: Note which domains or inline scripts are blocked
3. **Update policy**: Add necessary domains to the appropriate CSP directive
4. **Test thoroughly**: Ensure all site features work with the updated policy

For complex customizations, consider using the `csp-directives` option to define a completely custom policy.