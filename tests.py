from unittest import TestCase
from unittest import mock
from unittest.mock import patch, mock_open
from io import StringIO

from main import choose_random_student, readfile, send_email

def mock_csv_data():
    return """\
a@a.com,Bell,Ana,60,good,70,better,80,best
b@b.com,Pop,Banana,10,worst,20,bad,30,ok"""

class TestAcceptanceTest(TestCase):
    def test_read_in_csv_and_send_email(self):

        # First read in CSV file

        with patch("builtins.open", mock_open(read_data=mock_csv_data())) as mock_file:
            student_list = readfile('/path/to/open')

            with mock.patch.dict('os.environ', {
            'EMAIL_LOGIN': 'test@test.co.uk',
            'EMAIL_PASS': 'password'
            }):
                with patch('smtplib.SMTP_SSL', autospec=True) as mock_smtp:
                    with patch('main.choose_random_student') as mock_choose_random_student:
                        mock_choose_random_student.return_value = 'b@b.com'

                        send_email(student_list)

                        instance = mock_smtp.return_value
                        
                        self.assertEqual(instance.login.call_count, 2)
                        self.assertEqual(instance.sendmail.call_count, 2)
                        self.assertEqual(instance.quit.call_count, 2)

                        self.assertEqual(instance.sendmail.mock_calls[0][1][0], 'lecture@example.com')
                        self.assertEqual(instance.sendmail.mock_calls[0][1][1], 'a@a.com')
                        self.assertIn('Dear Bell', instance.sendmail.mock_calls[0][1][2])
                        self.assertNotIn('You\'ve been randomly', instance.sendmail.mock_calls[0][1][2])

                        self.assertEqual(instance.sendmail.mock_calls[1][1][0], 'lecture@example.com')
                        self.assertEqual(instance.sendmail.mock_calls[1][1][1], 'b@b.com')
                        self.assertIn('Dear Pop', instance.sendmail.mock_calls[1][1][2])
                        self.assertIn('You\'ve been randomly', instance.sendmail.mock_calls[1][1][2])


class TestCSV(TestCase):

    def test_can_read_csv(self):  
        with patch("builtins.open", mock_open(read_data=mock_csv_data())) as mock_file:
            readfile("path/to/open")
        mock_file.assert_called_with("path/to/open", "r")

    def test_read_line_to_dictionary(self):
        with patch("builtins.open", mock_open(read_data=mock_csv_data())) as mock_file:
            students = readfile("path/to/open")
        self.assertIn("a@a.com", students)


class TestEmail(TestCase):

    def test_send_test_email(self):

        student_results = {
            'test.send@example.com': {
                'first_name': 'test_first',
                'last_name':  'test_last',
                'problem1_score': 34,
                'problem1_comments': 'bad',
                'problem2_score': 60,
                'problem2_comments': 'good',
                'problem3_score': 90,
                'problem3_comments': 'great',
            }
        }
        
        with mock.patch.dict('os.environ', {
            'EMAIL_LOGIN': 'test@test.co.uk',
            'EMAIL_PASS': 'password'
            }):
            with patch('smtplib.SMTP_SSL', autospec=True) as mock_smtp:
                send_email(student_results)

                instance = mock_smtp.return_value
                
                self.assertTrue(instance.login.called)
                self.assertEqual(instance.login.call_count, 1)
                self.assertEqual(instance.login.mock_calls[0][1][0], 'test@test.co.uk')
                self.assertEqual(instance.login.mock_calls[0][1][1], 'password')

                self.assertTrue(instance.sendmail.called)
                self.assertEqual(instance.sendmail.call_count, 1)
                
                self.assertEqual(instance.sendmail.mock_calls[0][1][0], 'lecture@example.com')
                self.assertEqual(instance.sendmail.mock_calls[0][1][1], 'test.send@example.com')
                self.assertIn('Dear test_first', instance.sendmail.mock_calls[0][1][2])
                
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
        
           
         
