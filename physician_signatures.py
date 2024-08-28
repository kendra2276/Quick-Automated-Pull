​
# libraries
import glob
import pandas as pd
import os
import pyodbc
import numpy as np
from sqlalchemy import create_engine, text
import urllib.parse
import sys
import smtplib

# pulling in two additional  python scripts. The functions script contains resuable functions and the sql_scripts contains the sql code for this data pull.
from functions import functions as f
from sql_scripts import physician as sql

# pulling in  functions that contain the sql username/password, the email template for sending an email, and the error handling script. 
sys.path.insert(0, 'C:/')
from SQL_Login import sql_alchemy as sql_a
sys.path.insert(0, 'C:/Email_Templates/')
from excel_multiple_files import sending_multiple_files as s
sys.path.insert(0, 'C:/Kendra/DOH/')
from Email import email_header as eh



def main():
  # connecting to the sql database
  
    connection_string = sql_a.connection_string
    engine = create_engine(connection_string)
    conn = engine.connect()
  
  # pulling in the data from the sql script using pandas read_sql function
    tox = pd.read_sql(sql.physician, conn)

  # formating dates to be used in the body of the email.
    min = tox['SampleReceivedDT'].agg(['min']).astype("string")
    min = min.to_string(index=False)
    max = tox['SampleReceivedDT'].agg(['max']).astype("string")
    max = max.to_string(index=False)
  

  """ 
    By pulling in data on a weekly basis  this can lead to missing reports. This is due to the lab having to re-run assay or a hold up in the lab. The perfered method for doing an automated pull that
    factors in the reflexing would be a monthly pull or a daily pull. Since this was weekly, I went ahead and wrote a script that pulls in all of the previous reports, filters those reports out, and then gives 
    me the reports that need to go out for that week. Lastly, I wrapped this in a try except in case a report threw an error with the filtering. 
    """
    try:
        phy_path = f.csv_filepath()
        phy_filenames = glob.glob(phy_path + "/*.csv")
        dfs = []
        for filename in phy_filenames:
            phy = pd.read_csv(filename)
            phy['filename'] = filename 
            dfs.append(phy)

        phy = pd.concat(dfs, ignore_index=True)
        phy = phy[phy.columns[phy.columns.isin(['ProcessId', 'filename'])]]
        phy.drop_duplicates(inplace=True)

        tox = tox.loc[~tox['ProcessId'].isin(phy['ProcessId'])]

        outpath = f.csv_filepath()
        tox_filename = str('TOX No Physician Signature') + '_' + str(f.getToday())
        tox.to_csv(outpath + (str(tox_filename + '.csv')), index=False)

    """ 
    This exception clause will send an error message to my project management board using a pre defined template. 
    """
    except Exception as e:
        error_subject = "TOX - No Physician Signature"
        msg = eh.email_header(error_subject)
        msg.set_content(f"{e}")
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.starttls()
            smtp.login(eh.email_address, eh.email_pass)
            smtp.send_message(msg)
        sys.exit(1)


  """ 
  Sending an email using a built in function. 
  Allows for multiple emails to go within the variable called recipient_email.
  Uses HTML to format the body of the email and uses the blue color to allow for the date range to stand out. 
  Also lets the end user know if there are any new reports for the week. 
  Lastly, if the length of the reports is greater than zero, it attaches the file to the email. If there are no new reports then a file will not be attached to the email however an email will 
  still go out to the end user letting them know that there are no new reports. 
  """

    recipient_email = '''
    '''

    subject = f' TOX - No Physician Signature'
    body_of_email = f""" <html>
        <head></head>
        <body>
          <p>Hello.
          <br>
          <p>Please see the attached TOX - No Physician Signature report from <span style="color:blue;"> {min} to {max} </span>.</p>
          <ul>
              <li> There are {tox_length} reports. </li>
              <li> Only filtered that was applied was on the physician signature where physician signature equals no.</li>
          </ul>
          <p>
          Please let me know if you have any questions, comments, or concerns.
          <br>
          <br>
            Thank you,
            <br>
            Kendra
          </p>
        </body>
      </html>
      """

    file_path = outpath
    if tox_length > 0:
        filename = [f"{tox_filename}.csv"]
    else:
        filename = []
    monday = 'project managment board'
    eh_subject = 'TOX - No Physician Signature Report Data Query Error'
    s.sending_email(recipient_email, subject, body_of_email, file_path, filename, monday, eh_subject)

if __name__ == "__main__":
    main()
