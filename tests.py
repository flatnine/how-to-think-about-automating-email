from unittest import TestCase
from unittest import mock
from unittest.mock import patch, mock_open
from io import StringIO

from main import choose_random_student, readfile, send_email

class TestCSV(TestCase):

    def mock_csv_data(self):
        return """\
a@a.a,Bell,Ana,60,good,70,better,80,best
b@b.b,Pop,Banana,10,worst,20,bad,30,ok"""
    
    def test_can_read_csv(self):  
        with patch("builtins.open", mock_open(read_data=self.mock_csv_data())) as mock_file:
            readfile("path/to/open")
        mock_file.assert_called_with("path/to/open", "r")

    def test_read_line_to_dictionary(self):
        with patch("builtins.open", mock_open(read_data=self.mock_csv_data())) as mock_file:
            students = readfile("path/to/open")
        self.assertIn("a@a.a", students)


class TestEmail(TestCase):

    def test_send_test_email(self):
        
        with mock.patch.dict('os.environ', {
            'EMAIL_LOGIN': 'test@test.co.uk',
            'EMAIL_PASS': 'password'
            }):
            with patch('smtplib.SMTP_SSL', autospec=True) as mock_smtp:
                send_email()

                instance = mock_smtp.return_value
                
                self.assertTrue(instance.login.called)
                self.assertEqual(instance.login.call_count, 1)
                self.assertEqual(instance.login.mock_calls[0][1][0], 'test@test.co.uk')
                self.assertEqual(instance.login.mock_calls[0][1][1], 'password')

                self.assertTrue(instance.sendmail.called)
                self.assertEqual(instance.sendmail.call_count, 1)
                
                self.assertEqual(instance.sendmail.mock_calls[0][1][0], 'test@test.co.uk')
                self.assertEqual(instance.sendmail.mock_calls[0][1][1], 'test.send@example.com')
                self.assertEqual(instance.sendmail.mock_calls[0][1][2], 'this message is from python')
                
                self.assertTrue(instance.quit.called)
                self.assertEqual(instance.quit.call_count, 1)
           
    def test_choose_random_user(self):

        student_list = {
            'a@a.com': {},
            'b@b.com': {},
            'c@c.com': {},
        }
        student = choose_random_student(student_list)
        self.assertIn(student, student_list)
        
           
         
