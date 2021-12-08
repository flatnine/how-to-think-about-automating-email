from unittest import TestCase
from unittest.mock import patch, mock_open
from io import StringIO

from main import readfile

class TestCSV(TestCase):

    def mock_csv_data(self):
        return """\
Day,MxT,MnT,AvT,AvDP,1HrP TPcn,PDir,AvSp,Dir,MxS,SkyC,MxR,Mn,R AvSLP\n
1,88,59,74,53.8,0,280,9.6,270,17,1.6,93,23,1004.5
2,79,63,71,46.5,0,330,8.7,340,23,3.3,70,28,1004.5"""
    
    def test_can_read_csv(self):  
        with patch("builtins.open", mock_open(read_data=self.mock_csv_data())) as mock_file:
            readfile("path/to/open")
        mock_file.assert_called_with("path/to/open", "r")
