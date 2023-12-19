reset_password_template = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
    <style type="text/css">

    </style>
</head>
<body style="margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td style="padding: 20px 0 30px 0;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
    <tr>
    <td align="center" bgcolor="#007CC7" style="padding: 40px 0 30px 0;">
        <img src="https://private-user-images.githubusercontent.com/85158665/291017513-c996a1d4-dea7-45e3-9068-7974aeb065e3.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDMwMjE5MjMsIm5iZiI6MTcwMzAyMTYyMywicGF0aCI6Ii84NTE1ODY2NS8yOTEwMTc1MTMtYzk5NmExZDQtZGVhNy00NWUzLTkwNjgtNzk3NGFlYjA2NWUzLmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMTklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjE5VDIxMzM0M1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWQ5OTI4NmJiYzA5NWIzNGM0ZWVmZDdmNTVlZjVmYzNkMTljZTdlZGRhNjBmYTI0NDE1OGE4NzU2Yzc3MTQ5ODMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.0heFrKzgqWfWK5KlzYU9-VYmTgfXxQ2DoydGuI9c8BE" alt="KnowAfrika API logo" style="width:20%;heigh:0%;">
    </td>
    </tr>
    <tr>
    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
    <tr>
            <td style="color: #153643; font-family: Arial, sans-serif;">
            <h1 style="font-size: 24px; margin: 0;"></h1>
    </td>
    </tr>
        <tr>
            <td style="color: #153643; font-family: Roboto, sans-serif; font-size: 20px; line-height: 24px; padding: 20px 0 30px 0;">
       
                <h3> <p>Dear User,</p> </h3> </div>
               

                    <p>You have requested to change your password.</p>
                       
                        <p>Due to security reasons, we have provided you with a new code to reset your password</p>
                       
                        <strong><p>{code}</strong></br></p>
                       
                        Please note that this code will expire 
                        <strong>in a few minutes</strong> <br/>
                       
                        Thank You. <br/>
                        KnowAfrika Admin
                    </strong> 
                    </p>


            </td>
        </tr>
        <tr>
            <td>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                <tr>
                <td width="260" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                   
                    </table>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
    <tr>
    <td bgcolor="#007CC7" style="padding: 30px 30px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
        <tr>
            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
            <p style="margin: 0;">&reg; KnowAfrika API<br/>
           
            </td>
            <td align="right">
            <table border="0" cellpadding="0" width="100%" cellspacing="0" style="border-collapse: collapse;">
                <tr>
       
                <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
               
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </td>
    </tr>
</table>
        </td>
    </tr>
    </table>
</body>
</html>
"""
