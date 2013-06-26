"""This class creates a simple way of toggling between production and
development versions of css and js aggregate scripts.  The simplest way to
use this would be something like:

    css = CssAssets(devel=is_devel, asset_path="static")
    print css.add_asset('bootstrap.min.css')
    print css.add_asset('other.css')
    print css.add_asset('last.css')
    print css.render()

if is_devel is True, the above will print out three <script> tags:
    <link href="/static/css/bootstrap.min.css" type='text/css' rel='stylesheet'>
    <link href="/static/css/other.css" type='text/css' rel='stylesheet'>
    <link href="/static/css/last.css" type='text/css' rel='stylesheet'>

otherwise, if is_devel is False, the above will combine all of the above files
together into a single file, named the sha1 hash of the modification times
and file names of all the above assets.  This will be written to disk, and
render() will print out something like (the add asset calls will do nothing):

    <link href="/static/css/aggregate/{hash}.css" type='text/css' rel='stylesheet'>

The JavascriptAssets class does the same thing as the above, for JS assets

"""

import os


class AssetBase(object):

    def __init__(self, devel=True, asset_path="static"):
        self.devel = devel
        self.scripts = []
        self.asset_path = asset_path

    def add_asset(self, path):
        if self.devel:
            return self.__class__.script_tag(path)
        else:
            self.scripts.append(os.path.join(self.asset_path, self.__class__.SUBDIR, path))
            return ""

    def render(self):
        if self.devel:
            return ""
        else:
            import hashlib
            h = hashlib.sha1()

            # first, hash the name of all the assets we might aggregate.  If
            # the hash already exists on disk, don't do anything further
            script_summaries = [str(os.path.getmtime(s)) + "-" + s for s in self.scripts]
            h.update("-".join(script_summaries))
            file_name = h.hexdigest() + '.' + self.__class__.SUBDIR
            file_path = os.path.join(self.asset_path, self.__class__.SUBDIR, 'aggregate', file_name)
            if not os.path.isfile(file_path):
                contents = ""
                for script in self.scripts:
                    handle = open(script, 'r')
                    contents += handle.read()
                    handle.close()
                h = hashlib.sha1()
                h.update(contents)
                w_handle = open(file_path, 'w')
                w_handle.write(contents)
                w_handle.close()
            self.scripts = []
            return self.__class__.script_tag("aggregate/" + file_name)


class JavascriptAssets(AssetBase):

    SUBDIR = "js"

    @staticmethod
    def script_tag(path):
        return "<script src='/static/js/{0}'></script>".format(path)


class CssAssets(AssetBase):

    SUBDIR = "css"

    @staticmethod
    def script_tag(path):
        return "<link href='/static/css/{0}' type='text/css' rel='stylesheet'>".format(path)
