import unittest
import download
from os.path import exists

class TestDownloadMethods(unittest.TestCase):

    def test_download_invalidlink(self):
        url = "html://www.google.com"
        fname = "tests.pdf"
        self.assertEqual(download.download_pdf(url,fname),(False,"Invalid url schema"))

    def test_download_404(self):
        url = "https://www.google.com/hrtr"
        fname = "tests.pdf"
        self.assertEqual(download.download_pdf(url,fname),(False,"Error status code 404"))

    def test_download_timeout(self):
        url = "http://www.google.com:81/"
        fname = "tests.pdf"
        self.assertEqual(download.download_pdf(url,fname),(False, "Connection error"))
    
    def test_download_success(self):
        url = "https://file-examples-com.github.io/uploads/2017/10/file-sample_150kB.pdf"
        fname = "tests.pdf"
        self.assertEqual(download.download_pdf(url,fname),(True,fname))

class TestExcelMethods(unittest.TestCase):

    def test_import_excel(self):
        filename = "testexcel.xlsx"
        (imported,df) = download.import_excel_data(filename)
        self.assertIsNotNone(df)
        self.assertTrue(imported)

    def test_import_excel_invalid_filetype(self):
        filename = "download.py"
        (imported,df) = download.import_excel_data(filename)
        self.assertIsNone(df)
        self.assertFalse(imported)

    def test_import_excel_invalid_filename(self):
        filename = "idonotexist.xlsx"
        (_,df) = download.import_excel_data(filename)
        self.assertIsNone(df)

    def test_save_excel(self):
        filename = "testexcel.xlsx"
        (_,data) = download.import_excel_data(filename)
        output_name = "testsuccess.xlsx"
        download.save_excel_data(data,output_name)
        self.assertTrue(exists(output_name))
    
    def test_get_url_success(self):
        filename = "testexcel.xlsx"
        (_,df) = download.import_excel_data(filename)
        self.assertIsNotNone(download.get_urls_from_dataframe(df))

    def test_get_url_fail(self):
        filename = "testexcel2.xlsx"
        (_,df) = download.import_excel_data(filename)
        self.assertIsNone(download.get_urls_from_dataframe(df))

class TestCheckPdfFile(unittest.TestCase):

    def test_check_pdf_file_valid(self):
        filename = "tests.pdf"
        self.assertTrue(download.check_pdf_file(filename))

    def test_check_pdf_file_invalid(self):
        filename = "notpdf.pdf"
        self.assertFalse(download.check_pdf_file(filename))

    def test_check_pdf_file_nofile(self):
        filename = "idonotexist.pdf"
        self.assertFalse(download.check_pdf_file(filename))


        
if __name__ == '__main__':
    unittest.main()