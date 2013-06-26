pywebassets
===============

Tools for aggregating and compressing CSS and JS in production

Usage
===

This class creates a simple way of toggling between production and
development versions of css and js aggregate scripts.  The simplest way to
use this would be something like:

    css = CssAssets(devel=is_devel, asset_path="static")
    print css.add_asset('bootstrap.min.css')
    print css.add_asset('other.css')
    print css.add_asset('last.css')
    print css.render()

if is_devel is True, the above will print out three `<script>` tags:

    <link href="/static/css/bootstrap.min.css" type='text/css' rel='stylesheet'>
    <link href="/static/css/other.css" type='text/css' rel='stylesheet'>
    <link href="/static/css/last.css" type='text/css' rel='stylesheet'>

otherwise, if is_devel is False, the above will combine all of the above files
together into a single file, named the sha1 hash of the modification times
and file names of all the above assets.  This will be written to disk, and
render() will print out something like (the add asset calls will do nothing):


    <link href="/static/css/aggregate/{hash}.css" type='text/css' rel='stylesheet'>

The JavascriptAssets class does the same thing as the above, for JS assets
