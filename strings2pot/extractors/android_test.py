# -*- coding: utf-8 -*-

import os
import unittest
import android

class AndroidExtractorTest(unittest.TestCase):
    def setUp(self):
        self.mock_source_file = 'mock_source_android.xml'
        self.mock_destination_file = 'mock_destination_android.pot'
        def mock_context_id_generator(s): return 'MOCK_CONTEXT_ID'
        self.mock_context_id_generator = mock_context_id_generator

        with open(self.mock_source_file, 'a') as source_file:
            source_file.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
  <string name="string_name">Hello "%1$s", nice to see you here!</string>
</resources>
            """)
    
    def tearDown(self):
        try:
            os.unlink(self.mock_source_file)
            os.unlink(self.mock_destination_file)
        except Exception, e:
            pass

    # test that the AndroidExtractor class constructor sets source_file and destination_file attributes
    def test_ctor(self):
        sut = android.AndroidExtractor(
            self.mock_source_file,
            self.mock_destination_file,
            self.mock_context_id_generator
        )

        self.assertEqual(sut.source_file, self.mock_source_file)
        self.assertEqual(sut.destination_file, self.mock_destination_file)
    
    # test that AndroidExtractor parse_string method converts string in POT format 
    def test_parse_string(self):
        sut = android.AndroidExtractor('', '', self.mock_context_id_generator)

        single_line_string = "\' \" %1$d %2$s"
        self.assertEqual(
            sut.parse_string(single_line_string),
            '"\' \\\" %d %s"'
        )

        multi_line_string = "\' \" \\n %1$s %1$d"
        self.assertEqual(
            sut.parse_string(multi_line_string),
            '''""
"\' \\\" \\n"
" %s %d"'''
        )
    
    # test that AndroidExtractor run method converts an input file in POT format
    def test_run(self):
        sut = android.AndroidExtractor(
            self.mock_source_file,
            self.mock_destination_file,
            self.mock_context_id_generator
        )

        sut.run()

        with open(self.mock_destination_file, 'r') as destination_file:
            lines = destination_file.readlines()
            pot_content_as_string = "".join(lines)

            self.assertEqual(
                pot_content_as_string,
                '''
#: mock_source_android.xml:3
msgctxt "MOCK_CONTEXT_ID"
msgid "Hello \\\"%s\\\", nice to see you here!"
msgstr ""
'''
            )

if __name__ == '__main__':
    unittest.main()