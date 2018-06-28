#!/usr/bin/env python

import os
import sys
import unittest
import Cheetah.ImportHooks
from Cheetah.LoadTemplate import loadTemplateClass
from Cheetah.Tests.ImportHooks import ImportHooksTemplatesDir, _cleanup
from Cheetah.Tests.ImportHooks import setUpModule, tearDownModule  # noqa


class LoadTemplateTest(unittest.TestCase):
    def setUp(self):
        _cleanup()

    def test_loadTemplate(self):
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertNotIn('index.py', templates)
        self.assertNotIn('layout.py', templates)
        self.assertRaises(ImportError, loadTemplateClass,
                          os.path.join(ImportHooksTemplatesDir, 'index.tmpl'))
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertIn('index.py', templates)
        self.assertNotIn('layout.py', templates)

        loadTemplateClass(
            os.path.join(ImportHooksTemplatesDir, 'layout.tmpl'))
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertIn('index.py', templates)
        self.assertIn('layout.py', templates)

        loadTemplateClass(
            os.path.join(ImportHooksTemplatesDir, 'index.tmpl'))

    def test_ImportHooks(self):
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertNotIn('index.py', templates)
        self.assertNotIn('layout.py', templates)
        Cheetah.ImportHooks.install()
        loadTemplateClass(
            os.path.join(ImportHooksTemplatesDir, 'index.tmpl'))
        templates = os.listdir(ImportHooksTemplatesDir)
        self.assertIn('index.py', templates)
        self.assertIn('layout.py', templates)
        Cheetah.ImportHooks.uninstall()
        for modname in list(sys.modules.keys()):
            if '.ImportHooksTemplates.' in modname \
                    or modname.endswith('.ImportHooksTemplates'):
                del sys.modules[modname]
        del sys.modules['index']
        del sys.modules['layout']


if __name__ == '__main__':
    unittest.main()
