# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import tempfile

from demo import config

logger = logging.getLogger(__name__)


class GDriveService(object):
    """Service to write to a spread sheet in google drive."""

    # Name of the spreadsheet
    SPREADSHEET_NAME = "Sales requests"

    # Sheet where the new address change entries should be stored in
    SHEET_NAME = "Sheet1"

    def __init__(self, gdrive_credentials_json=config.gdrive_credentials):
        scopes = ['https://spreadsheets.google.com/feeds',
                  'https://www.googleapis.com/auth/drive']
        with tempfile.NamedTemporaryFile(suffix="_credentials.json") as f:
            f.write(gdrive_credentials_json)
            f.flush()
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
                                                            f.name,
                                                            scopes=scopes)

    def request_sheet(self, sheet_name):
        logging.debug("Refreshing auth")
        try:
            return gspread.authorize(self.credentials).open(sheet_name)
        except Exception as e:
            logging.error("Failed to create google spreadsheet connection. %s",
                          e, exc_info=True)
            return None

    def store_data(self, data):
        """Adds a single new row to the sheet containing the users name and
        address."""
        self.append_row(self.SPREADSHEET_NAME, data,
                        self.SHEET_NAME)

    def append_row(self, sheet_name, row_values, worksheet_name):
        sheet = self.request_sheet(sheet_name)
        try:
            worksheet = sheet.worksheet(worksheet_name)
            if worksheet is not None:
                worksheet.append_row(row_values)
        except Exception as e:
            logging.error("Failed to write row to gdocs. Sheet %s/%s. Error: %s",
                          sheet_name, worksheet_name, e, exc_info=True)
