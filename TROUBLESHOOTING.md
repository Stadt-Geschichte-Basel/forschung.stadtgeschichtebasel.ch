# Troubleshooting Guide

This guide helps you resolve common issues when working with the forschung.stadtgeschichtebasel.ch project.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Build and Serve Issues](#build-and-serve-issues)
- [Data Processing Issues](#data-processing-issues)
- [Display and Rendering Issues](#display-and-rendering-issues)
- [Performance Issues](#performance-issues)
- [Common Error Messages](#common-error-messages)
- [Getting Additional Help](#getting-additional-help)

## Installation Issues

### Ruby Version Conflicts

**Problem**: Error message about Ruby version mismatch

```
Your Ruby version is X.X.X, but your Gemfile specified Y.Y.Y
```

**Solutions**:

1. **Using rbenv** (recommended):

```bash
# Install the correct Ruby version
rbenv install 2.7.0
rbenv local 2.7.0

# Verify
ruby --version
bundle install
```

2. **Using rvm**:

```bash
# Install the correct Ruby version
rvm install 2.7.0
rvm use 2.7.0

# Verify
ruby --version
bundle install
```

3. **Update Gemfile** (if you need to use a different Ruby version):

Edit `Gemfile` and change the Ruby version requirement.

### Bundle Install Fails

**Problem**: Gem installation errors

```
An error occurred while installing [gem-name]
```

**Solutions**:

1. **Install build tools**:

```bash
# macOS
xcode-select --install

# Ubuntu/Debian
sudo apt-get install build-essential libssl-dev

# Fedora/RHEL
sudo dnf install gcc gcc-c++ make openssl-devel
```

2. **Install missing dependencies**:

```bash
# For nokogiri issues (common)
# macOS
brew install libxml2 libxslt

# Ubuntu/Debian
sudo apt-get install libxml2-dev libxslt1-dev

# Then retry
bundle install
```

3. **Clear bundle cache and retry**:

```bash
bundle clean --force
rm -rf vendor/bundle
bundle install
```

### Node.js/npm Issues

**Problem**: npm install fails or packages are missing

**Solutions**:

1. **Clear npm cache**:

```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

2. **Update npm**:

```bash
npm install -g npm@latest
```

3. **Check Node.js version**:

```bash
node --version  # Should be 18.x or higher
```

If your version is too old, [download and install the latest LTS version](https://nodejs.org/).

### Python/uv Issues

**Problem**: uv command not found or Python package installation fails

**Solutions**:

1. **Install or reinstall uv**:

```bash
# Using pip
pip install --upgrade uv

# Or using pipx (recommended)
pipx install uv
```

2. **Verify Python version**:

```bash
python --version  # Should be 3.9 or higher
```

3. **Reset Python environment**:

```bash
rm -rf .venv
uv sync
```

## Build and Serve Issues

### Port Already in Use

**Problem**: `Address already in use - bind(2) for 127.0.0.1:4000`

**Solutions**:

1. **Use a different port**:

```bash
bundle exec jekyll serve --port 4001
```

2. **Find and kill the process using port 4000**:

```bash
# macOS/Linux
lsof -ti:4000 | xargs kill -9

# Windows
netstat -ano | findstr :4000
taskkill /PID [PID] /F
```

### Jekyll Build Fails

**Problem**: Errors during `bundle exec jekyll build` or `npm run dev`

**Common causes and solutions**:

1. **Syntax errors in Liquid templates**:

Check the error message for the file and line number. Common issues:

- Unclosed tags: `{% if %}` without `{% endif %}`
- Invalid variable names: `{{ site.non-existent-var }}`
- Malformed filters: `{{ page.title | filter: }}`

2. **Missing or corrupt data files**:

```bash
# Clean generated files
npm run clean

# Regenerate data
npm run populate
```

3. **Invalid YAML frontmatter**:

Check for:

- Proper indentation (2 spaces)
- Quotes around strings with special characters
- Valid YAML syntax

### Auto-Regeneration Not Working

**Problem**: Changes to files don't trigger rebuild

**Solutions**:

1. **Check if the file is in an excluded directory** (like `vendor/` or `node_modules/`)

2. **Restart the server**:

```bash
# Stop with Ctrl+C, then restart
npm run dev
```

3. **Use polling** (slower but more reliable):

```bash
bundle exec jekyll serve --force_polling
```

### CSS or JavaScript Not Loading

**Problem**: Styles or scripts are not applying

**Solutions**:

1. **Clear browser cache**:

   - Chrome/Firefox: Ctrl+Shift+Delete (Cmd+Shift+Delete on Mac)
   - Or use hard refresh: Ctrl+Shift+R (Cmd+Shift+R on Mac)

2. **Check browser console** for errors (F12 to open developer tools)

3. **Verify asset paths** in your templates

4. **Check if files are being generated**:

```bash
ls -la _site/assets/css/
ls -la _site/assets/js/
```

## Data Processing Issues

### Omeka API Connection Fails

**Problem**: `npm run populate` fails with connection or authentication errors

**Solutions**:

1. **Verify your `.env` file** exists and has correct values:

```bash
cat .env  # Should show your API credentials
```

2. **Check API credentials**:

   - Log in to [Omeka S](https://omeka.unibe.ch)
   - Go to your user profile → API Keys
   - Generate new keys if needed
   - Update `.env` with new values

3. **Test API connection**:

```bash
curl -H "key_identity: YOUR_KEY" -H "key_credential: YOUR_CREDENTIAL" \
  https://omeka.unibe.ch/api/items?item_set_id=10780
```

### No Items Display

**Problem**: The site builds but no collection items appear

**Solutions**:

1. **Check if metadata files exist**:

```bash
ls -la _data/sgb-metadata-*
```

2. **Verify metadata file is referenced in `_config.yml`**:

```yaml
metadata: sgb-metadata-csv # Should match your CSV filename
```

3. **Regenerate data**:

```bash
npm run clean
npm run populate
npm run dev
```

4. **Check for errors in metadata CSV**:

   - Open `_data/sgb-metadata-csv.csv`
   - Verify columns are properly formatted
   - Check for encoding issues (should be UTF-8)

### Media Objects Not Loading

**Problem**: Items display but images/media don't load

**Solutions**:

1. **Check if object files exist**:

```bash
ls -la objects/
```

2. **Verify object IDs** in metadata match actual files

3. **Check file permissions**:

```bash
chmod 644 objects/*
```

4. **Look at browser console** for 404 errors

## Display and Rendering Issues

### Layout Broken or Incorrect

**Problem**: Pages don't display correctly

**Solutions**:

1. **Clear Jekyll cache**:

```bash
bundle exec jekyll clean
npm run dev
```

2. **Check for YAML errors** in frontmatter

3. **Verify layout file exists**:

```bash
ls -la _layouts/
```

### Timeline Not Displaying

**Problem**: Timeline page is blank or shows errors

**Solutions**:

1. **Check for EDTF date format** in metadata:

   - Dates should follow EDTF standard
   - Example: `1950`, `1950-05`, `1950-05-15`

2. **Verify temporal field** in metadata CSV

3. **Check browser console** for JavaScript errors

### Map Not Working

**Problem**: Map visualization doesn't load

**Solutions**:

1. **Check for valid coordinates** in metadata

2. **Verify GeoJSON format** for geodata items

3. **Check browser console** for Leaflet errors

4. **Ensure internet connection** (Leaflet requires external tiles)

### Search Not Working

**Problem**: Search returns no results or errors

**Solutions**:

1. **Check if Lunr.js index is built**:

```bash
ls -la _site/assets/data/
```

2. **Rebuild the site**:

```bash
bundle exec jekyll build
npm run dev
```

3. **Clear browser cache** and test again

## Performance Issues

### Slow Build Times

**Problem**: Jekyll takes a long time to build

**Solutions**:

1. **Use incremental builds** (default in development):

```bash
bundle exec jekyll serve --incremental
```

2. **Limit collection size during development**:

Edit `_config.yml` and add:

```yaml
limit_posts: 10 # Only process 10 items
```

3. **Exclude unnecessary files**:

Add to `_config.yml`:

```yaml
exclude:
  - vendor/
  - node_modules/
  - docs/
```

### Slow Page Load Times

**Problem**: Site loads slowly in browser

**Solutions**:

1. **Optimize images**:

```bash
# Use image optimization tools
# Example with ImageMagick:
mogrify -resize 1200x1200\> -quality 85 objects/*.jpg
```

2. **Enable lazy loading** (already implemented for images)

3. **Check browser network tab** to identify large resources

4. **Use production build** for final testing:

```bash
npm run build:production
```

## Common Error Messages

### `Liquid Exception: Liquid syntax error`

**Cause**: Invalid Liquid template syntax

**Fix**: Check the file and line number in the error, look for:

- Unclosed tags
- Invalid filters
- Malformed conditionals

### `YAML Exception: mapping values are not allowed`

**Cause**: Invalid YAML syntax in frontmatter or data files

**Fix**:

- Check for proper indentation
- Quote strings with special characters
- Ensure colons have spaces after them

### `LoadError: cannot load such file`

**Cause**: Missing Ruby gem or wrong paths

**Fix**:

```bash
bundle install
bundle exec jekyll serve
```

### `Error: ENOSPC`

**Cause**: File watcher limit exceeded (Linux)

**Fix**:

```bash
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## Getting Additional Help

If you've tried the solutions above and still have issues:

### 1. Check Existing Resources

- [README.md](README.md) - Project overview and basic setup
- [SETUP.md](SETUP.md) - Detailed setup instructions
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [docs/](docs/) - Technical documentation
- [CollectionBuilder Docs](https://collectionbuilder.github.io/cb-docs/) - Framework documentation

### 2. Search GitHub Issues

Search [existing issues](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/issues) for similar problems.

### 3. Ask in Discussions

Post in [GitHub Discussions](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/discussions) with:

- Description of the problem
- What you've tried
- Your environment (OS, Ruby/Node/Python versions)
- Relevant error messages

### 4. Open an Issue

If you've found a bug, [open an issue](https://github.com/Stadt-Geschichte-Basel/forschung.stadtgeschichtebasel.ch/issues/new) with:

- **Title**: Brief description of the problem
- **Description**: Detailed explanation
- **Steps to reproduce**: How to trigger the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**:
  - Operating System
  - Ruby version (`ruby --version`)
  - Node version (`node --version`)
  - Jekyll version (`bundle exec jekyll --version`)
- **Screenshots**: If applicable
- **Logs**: Relevant error messages

### Gathering Debug Information

Run these commands and include the output in your issue:

```bash
# System info
uname -a  # Or: ver (Windows)

# Versions
ruby --version
node --version
npm --version
bundle --version
bundle exec jekyll --version

# Jekyll verbose build
bundle exec jekyll build --verbose --trace

# Check for config issues
bundle exec jekyll doctor
```

## Additional Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [CollectionBuilder Support](https://collectionbuilder.github.io/cb-docs/docs/support/)
- [Jekyll Talk Forum](https://talk.jekyllrb.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/jekyll)

---

**Last updated**: 2025-11-11

Found an issue with this guide? [Contribute improvements!](CONTRIBUTING.md)
