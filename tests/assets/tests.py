import os

from staticassets import AssetAttributes
from staticassets.finder import StaticFilesFinder

from ..test import TestCase


class FindAssetTest(TestCase):
    def setUp(self):
        self.finder = StaticFilesFinder()

    def test_attributes_search_paths(self):
        self.assertEqual(['index.js', 'index/component.json'], AssetAttributes('index.js').search_paths)
        self.assertEqual(['foo.js', 'foo/index.js', 'foo/component.json'], AssetAttributes('foo.js').search_paths)

    def test_attributes_extensions(self):
        self.assertEqual(['.js', '.coffee'], AssetAttributes('foo.js.coffee').extensions)

    def test_attributes_path_without_extensions(self):
        self.assertEqual('foo/bar', AssetAttributes('foo/bar.js.coffee').path_without_extensions)

    def test_asset_source(self):
        self.assertEqual('//= require models\n\nvar App = {Models: {}};\n', self.finder.find('app.js').source)

    def test_asset_content(self):
        asset = self.finder.find('models/User.js')
        asset.content = '(function(){%s})' % asset.content
        self.assertEqual('(function(){App.Models.User = {};\n})', asset.content)

    def test_asset_path(self):
        self.assertEqual(self.fixture_path('models/index.js'), self.finder.find('models').path)

    def test_dependencies(self):
        asset = self.finder.find('app.js')

        app_file = self.fixture_path('app.js')
        models_file = self.fixture_path('models/index.js')
        user_file = self.fixture_path('models/User.js')

        self.assertItemsEqual([
            [app_file, os.path.getmtime(app_file), self.file_digest(app_file)],
            [models_file, os.path.getmtime(models_file), self.file_digest(models_file)],
            [user_file, os.path.getmtime(user_file), self.file_digest(user_file)]
        ], asset.dependencies)

    def test_requirements(self):
        asset = self.finder.find('app.js')

        self.assertEqual([
            self.finder.find('models/index.js').path,
        ], [a.path for a in asset.requirements])

        self.assertEqual([
            self.finder.find('models/User.js').path,
            self.finder.find('models/index.js').path,
            self.finder.find('app.js').path,
        ], [a.path for a in asset])
